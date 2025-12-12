from typing import Dict, Any, List
from .preprocessing import preprocess_text, split_sentences

def extract_features(chat_data: Dict[str, Any], context_data: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts features for evaluation from chat and context data."""
    
    # Assuming chat_data contains 'user_query' and 'ai_response' directly for simplicity
    # In a real scenario, we might need to parse a conversation list
    
    # Handle case where chat_data might be a list or dict
    conversation_list = []
    if isinstance(chat_data, list):
        conversation_list = chat_data
    elif isinstance(chat_data, dict):
        if 'conversation_turns' in chat_data:
            conversation_list = chat_data['conversation_turns']
        # Else it might be a single turn dict, handled below if list is empty
    
    query = ""
    response = ""

    if conversation_list:
        # Iterate to find last user and assistant messages
        for msg in reversed(conversation_list):
            role = msg.get('role', '').lower()
            content = msg.get('content', '') or msg.get('message', '') # Handle 'message' key in new samples
            
            is_ai = 'ai' in role or 'assistant' in role or 'model' in role or 'chatbot' in role
            is_user = 'user' in role
            
            if not response and is_ai:
                response = content
            elif not query and is_user:
                query = content
            
            if query and response:
                break
    
    if not query and not response:
        # Fallback for simple dict structure or if list parsing failed
        if isinstance(chat_data, dict):
             query = chat_data.get('user', '') or chat_data.get('query', '')
             response = chat_data.get('assistant', '') or chat_data.get('response', '') or chat_data.get('ai_response', '')
        elif isinstance(chat_data, list) and chat_data:
             last_turn = chat_data[-1]
             query = last_turn.get('user', '') or last_turn.get('query', '')
             response = last_turn.get('assistant', '') or last_turn.get('response', '') or last_turn.get('ai_response', '')

    features = {
        'query': query,
        'response': response,
        'clean_query': preprocess_text(query),
        'clean_response': preprocess_text(response),
        'response_sentences': split_sentences(response),
        
        # Context features
        'retrieval_count': len(context_data.get('vectors', [])),
        'context_chunks': [v.get('text', '') for v in context_data.get('vectors', [])],
        'context_tokens': context_data.get('total_context_tokens', 0),
        'source_urls': [v.get('source_url') for v in context_data.get('vectors', [])],
        'retrieval_scores': context_data.get('retrieval_scores', []),
        'average_relevance': 0.0 # Calculated below
    }

    if features['retrieval_scores']:
        features['average_relevance'] = sum(features['retrieval_scores']) / len(features['retrieval_scores'])

    return features
