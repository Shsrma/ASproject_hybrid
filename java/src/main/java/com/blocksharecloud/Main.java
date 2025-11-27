package com.blocksharecloud;

import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.*;
import java.net.InetSocketAddress;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws Exception {

        int port = 9000;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        // Register API Endpoints
        server.createContext("/verify", new VerifyHandler());
        server.createContext("/timezone", new TimezoneHandler());
        server.createContext("/translate", new TranslateHandler());

        // Thread pool executor
        server.setExecutor(Executors.newFixedThreadPool(10));

        System.out.println("✅ Java microservice running on http://127.0.0.1:" + port);
        server.start();
    }

    /* Helper: Send JSON + CORS */
    static void sendJson(HttpExchange t, String json, int status) throws IOException {
        t.getResponseHeaders().set("Content-Type", "application/json; charset=utf-8");
        t.getResponseHeaders().set("Access-Control-Allow-Origin", "*");
        byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
        t.sendResponseHeaders(status, bytes.length);
        try (OutputStream os = t.getResponseBody()) {
            os.write(bytes);
        }
    }
}

/* ---------------------------------------------------------
    VERIFY HANDLER
------------------------------------------------------------ */
class VerifyHandler implements HttpHandler {
    @Override
    public v
