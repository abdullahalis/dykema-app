# Dykema Command Line AI App

A conversational AI system integrating Supabase (Postgres + Auth), Redis caching, and modular LLM orchestration. Supports multiple conversations, row-level security, and efficient message retrieval.

## Features

- **Multi-Conversation Support**: Manage multiple conversations with seamless switching.  
- **Row-Level Security**: Supabase ensures users only access their own conversations.  
- **Caching**: Redis accelerates frequent reads and reduces DB load.  
- **Modular LLM**: Easily switch between Anthropic and OpenAI models, with streaming and context-aware responses.  
- **Optional RAG**: Integrate document-based retrieval for richer, context-aware replies.  

## Architecture & Design

- **Modularity**: Abstract base classes allow swapping storage, authentication, and LLM implementations.  
- **Separation of Concerns**: OrchestrationManager coordinates Auth, Storage, and LLM, keeping business logic decoupled from infrastructure.  
- **Performance**: CombinedStorageManager transparently integrates Redis caching with Supabase for low-latency reads.  
- **Extensibility**: New storage backends, LLM providers, or auth methods can be added without modifying core logic.  

## Installation

1. Clone the repository:  
   ```
   git clone https://github.com/abdullahalis/recipe-mobile-app.git
   ```
2. Place the provided .env file in the dykema-app folder.

3. Navigate to the project directory:
```
cd dykema-app
```
4. Create and activate a virtual environment:
```
python -m venv dykema-env
source dykema-env/bin/activate  # Mac/Linux
.\dykema-env\Scripts\Activate.ps1  # Windows PowerShell
```
5. Install dependencies:
```
pip install -r requirements.txt
```
6. Run the app:
```
python main.py
```
7. Optionally set USE_DOCUMENTS to True in config/settings.py to enable RAG responses using the Bondi v. Vanderstok case as reference.
8. Run tests:
```
python -m pytest -v -s
```

## Trade-offs & Future Extensions

- **Storage Choices**:  
  - **Supabase Only**: Secure with row-level security, but repeated reads of long conversations may be slower.  
  - **Supabase + Redis Caching**: Improves read performance and reduces DB load, but introduces added complexity and the risk of stale reads.

- **Modular LLM Design**:  
  - Allows switching providers and supports streaming responses.  
  - Trade-off: More complex orchestration and slightly higher initial setup effort.

- **Document-Based RAG (Retrieval-Augmented Generation)**:  
  - Enables richer, context-aware responses using external documents.  
  - Trade-off: Adds latency, storage requirements, and preprocessing overhead; disabled by default for speed.

- **Future Extensions**:  
  - Additional storage backends or caching layers.  
  - Integration with more LLM providers or custom models.  
  - Enhanced RAG pipelines for large document pool.  