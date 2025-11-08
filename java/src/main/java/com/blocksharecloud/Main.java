package com.blocksharecloud;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.ZoneId;
import java.util.Map;
import java.util.List;
import java.util.stream.Collectors;
import java.io.InputStream;

public class Main {
    public static void main(String[] args) throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress(9000), 0);
        server.createContext("/verify", new VerifyHandler());
        server.createContext("/timezone", new TimezoneHandler());
        server.createContext("/translate", new TranslateHandler());
        server.setExecutor(null);
        System.out.println("Java microservice listening on http://127.0.0.1:9000");
        server.start();
    }
}

class VerifyHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange t) throws IOException {
        String response = "";
        try (InputStream is = t.getRequestBody()) {
            String body = new String(is.readAllBytes(), StandardCharsets.UTF_8);
            // Very simple 'verification' - just echo back received block and say valid:true
            response = "{" + "\"status\":\"ok\",\"valid\":true,\"received\":" + jsonEscape(body) + "}";
        } catch (Exception e) {
            response = "{\"status\":\"error\",\"error\":\"" + e.getMessage() + "\"}";
        }
        sendJson(t, response);
    }
    private String jsonEscape(String s) {
        return '"' + s.replace("\"","\\\"") + '"';
    }
    private void sendJson(HttpExchange t, String response) throws IOException {
        t.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        t.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);
        try (OutputStream os = t.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }
}

class TimezoneHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange t) throws IOException {
        Map<String, String> query = QueryParser.parse(t.getRequestURI().getQuery());
        String region = query.getOrDefault("region", ZoneId.systemDefault().toString());
        ZonedDateTime now = ZonedDateTime.now(ZoneId.of(region));
        String dt = now.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME);
        String response = String.format("{\"timezone\":\"%s\",\"datetime\":\"%s\"}", region, dt);
        t.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        t.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);
        try (OutputStream os = t.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }
}

class TranslateHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange t) throws IOException {
        Map<String, String> query = QueryParser.parse(t.getRequestURI().getQuery());
        String lang = query.getOrDefault("lang", "en");
        String text = query.getOrDefault("text", "Hello");
        // Very basic pseudo-translation for demonstration
        String translated = text;
        if (lang.equals("hi")) translated = "[HI] " + text;
        if (lang.equals("es")) translated = "[ES] " + text;
        String response = String.format("{\"lang\":\"%s\",\"text\":\"%s\"}", lang, escape(translated));
        t.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        t.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);
        try (OutputStream os = t.getResponseBody()) {
            os.write(response.getBytes(StandardCharsets.UTF_8));
        }
    }
    private String escape(String s) {
        return s.replace("\"","\\\"").replace("\\","\\\\"); 
    }
}

// Simple query parser helper
class QueryParser {
    public static Map<String,String> parse(String q) {
        if (q == null || q.isEmpty()) return Map.of();
        return java.util.Arrays.stream(q.split("&")).map(s -> s.split("=",2)).filter(a -> a.length>0)
            .collect(Collectors.toMap(a -> urlDecode(a[0]), a -> a.length>1?urlDecode(a[1]):""));
    }
    private static String urlDecode(String s) {
        try { return java.net.URLDecoder.decode(s, StandardCharsets.UTF_8.name()); } catch(Exception e){ return s; }
    }
}
