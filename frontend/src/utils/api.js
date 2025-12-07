const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

export const askChatbot = async (query, highlightedText = '') => {
  try {
    const response = await fetch(`${API_BASE_URL}/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query, highlighted_text: highlightedText }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.answer;
  } catch (error) {
    console.error("Error asking chatbot:", error);
    return "Sorry, I'm having trouble connecting to the AI. Please try again later.";
  }
};

export const getDocuments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/documents`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.documents;
  } catch (error) {
    console.error("Error fetching documents:", error);
    return [];
  }
};

export const uploadDocument = async (file) => {
  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.message;
  } catch (error) {
    console.error("Error uploading document:", error);
    return "";
  }
};

export const deleteDocument = async (documentId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/delete/${documentId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.message;
  } catch (error) {
    console.error("Error deleting document:", error);
    return "";
  }
};

export const reindexDocuments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/reindex`, {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.message;
  } catch (error) {
    console.error("Error reindexing documents:", error);
    return "";
  }
};
