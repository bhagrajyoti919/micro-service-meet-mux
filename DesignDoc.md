# Microservices Architecture Design Document

## System Overview

This document describes a microservices-based e-commerce system consisting of two independent services: **User Service** and **Order Service**. The system demonstrates synchronous inter-service communication, resilience patterns, and fault tolerance mechanisms.

## Architecture Diagram

┌─────────────┐ HTTP/REST ┌─────────────┐
│ Client │────────────────────────────▶│ API Gateway │
│ (Postman) │ │ (Optional) │
└─────────────┘ └──────┬──────┘
│
┌──────────────────────────┼────────────────────────┐
│ │ │
▼ ▼ ▼
┌───────────────┐ ┌───────────────┐ ┌─────────────┐
│ User Service │◀─────────│ Order Service │ │ Other │
│ Port 8000 │ Sync │ Port 8001 │ │ Services │
└───────┬───────┘ HTTP └───────┬───────┘ └─────────────┘
│ │
▼ ▼
┌───────────────┐ ┌───────────────┐
│ Users DB │ │ Orders DB │
│ (In-Memory) │ │ (In-Memory) │
└───────────────┘ └───────────────┘