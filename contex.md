# Custom AI Chatbot for Students: Detailed Build Guide

This document provides an exhaustive, step-by-step blueprint for building a full-stack web application that enables students to interact with an AI chatbot. The app features:
- **Custom Chat Interface:** A friendly UI where users can chat with the AI.
- **Student-Focused Customization:** Options like “explain like a kid” to simplify explanations.
- **Internal Prompt Engineering:** Automatically refines user prompts before sending them to the AI.
- **Advanced Response Modes:** Switch between **Creative Mode** (for imaginative responses, using a temperature of 1.2) and **Accurate Mode** (for precise answers, using a temperature of 0.2).
- **Differentiation from ChatGPT:** Unique features such as multiple explanation modes, enhanced prompt processing, and an interactive UI.

---

## 1. Project Overview

### **Objective**
- **Primary Goal:** Build a user-friendly AI chatbot web app specifically designed for students. It should enable users to ask questions and receive answers in different styles.
- **Key Features:**
  - **Explanation Modes:** Allow users to toggle between a “normal” explanation and a “kid-friendly” explanation.
  - **Response Modes:** Let users switch between:
    - **Accurate Mode:** Lower temperature (0.2) for more factual and precise responses.
    - **Creative Mode:** Higher temperature (1.2) for more imaginative, open-ended responses.
  - **Prompt Engineering:** Automatically process and optimize prompts before sending them to the AI API (OpenRouter using the model `openai/gpt-4o-mini`).

### **Tech Stack**
- **Backend:** Python with Flask  
  - Libraries: Flask, requests, flask-cors  
  - API: OpenRouter API (using `openai/gpt-4o-mini`)
- **Frontend:** React.js  
  - Libraries: Axios, Create React App  
- **Deployment:**  
  - **Backend:** Render, Railway, or similar  
  - **Frontend:** Vercel, Netlify, or similar

---

## 2. Project Structure

Organize your project in a clear, modular way. 

