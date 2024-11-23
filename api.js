import axios from 'axios';

const apiClient = axios.create({
     baseURL: 'api-gateway-invoke-url',
     headers: {
       'Content-Type': 'application/json',
     },
   });

export const fetchNoAgentResponse = async (prompt) => {
     try {
       const response = await apiClient.post('/fetch-response', { prompt });
       return response.data;
     } catch (error) {
       console.error('Error fetching no agent response:', error);
       throw error;
     }
   };

export const fetchAgentResponse = async (prompt) => {
     try {
       const response = await apiClient.post('/agent-fetch-response', { prompt });
       return response.data;
     } catch (error) {
       console.error('Error fetching agent response:', error);
       throw error;
     }
   };

export const TranslateContent = async (sourceLanguage, targetLanguage, content) => {
  try {
    const response = await apiClient.post('/translate-ui-content', {
      sourceLanguage,
      targetLanguage,
      content
    });
    return response.data;
  } catch (error) {
    console.error('Error translating your content:', error);
    throw error;
  }
};
