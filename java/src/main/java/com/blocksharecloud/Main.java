package com.blocksharecloud;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.*;

public class Main {

    public static void main(String[] args) throws Exception {

        int port = 9000;

        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        server.createContext("/verify", new VerifyHandler());
        server.createContext("/timezone", new TimezoneHandler());
        server.createContext("/translate", new TranslateHandler());

        server.setExecutor(Executors.newFixedThreadPool(10));

        System.out.println("Java microservice running at http://127.0.0.1:" + port);
        server.start();
    }

    static void sendJson(HttpExchange t, String json, int status) throws IOException {
        t.getResponseHeaders().set("Content-Type", "application/json");
        t.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
        t.sendResponseHeaders(status, bytes.length);
        try (OutputStream os = t.getResponseBody()) {
            os.write(bytes);
        }
    }
}

class VerifyHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange t) throws IOException {

        String requestBody =
                new BufferedReader(new InputStreamReader(t.getRequestBody()))
                        .lines().reduce("", (a, b) -> a + b);

        String response =
                "{ \"status\": \"verified\", \"details\": " + requestBody + " }";

        Main.sendJson(t, response, 200);
    }
}

class TimezoneHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange t) throws IOException {

        Map<String, String> queryParams = new HashMap<>();

        String q = t.getRequestURI().getRawQuery();
        if (q != null) {
            for (String p : q.split("&")) {
                String[] kv = p.split("=");
                if (kv.length == 2) {
                    queryParams.put(kv[0], kv[1]);
                }
            }
        }

        String region = queryParams.getOrDefault("region", "UTC");

        ZoneId zone = ZoneId.of(region);
        ZonedDateTime now = ZonedDateTime.now(zone);

        String json =
                "{ \"timezone\": \"" + region + "\", " +
                        "\"datetime\": \"" + now.format(DateTimeFormatter.ISO_OFFSET_DATE_TIME) + "\" }";

        Main.sendJson(t, json, 200);
    }
}

class TranslateHandler implements HttpHandler {
    @Override
    public void handle(HttpExchange t) throws IOException {

        String q = t.getRequestURI().getRawQuery();
        Map<String, String> params = new HashMap<>();

        if (q != null) {
            for (String p : q.split("&")) {
                String[] kv = p.split("=");
                if (kv.length == 2) {
                    params.put(kv[0], kv[1]);
                }
            }
        }

        String text = params.getOrDefault("text", "Hello");
        String lang = params.getOrDefault("lang", "en");

        String json =
                "{ \"text\": \"" + text + "\", \"lang\": \"" + lang + "\" }";

        Main.sendJson(t, json, 200);
    }
}
