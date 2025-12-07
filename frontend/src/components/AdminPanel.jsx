import React, { useState, useEffect } from 'react';
import './AdminPanel.css'; // Optional CSS file

const AdminPanel = () => {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);

  // Backend API base URL
  const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000';

  // Fetch documents from backend
  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/documents`);
      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      } else {
        console.error('Failed to fetch documents:', response.statusText);
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
    } finally {
      setLoading(false);
    }
  };

  // Handle file upload
  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setUploadStatus('Please select a file to upload');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    setUploadStatus('Uploading...');
    try {
      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        setUploadStatus('Upload successful!');
        setSelectedFile(null);
        // Reset file input
        const fileInput = document.getElementById('file-upload');
        if (fileInput) fileInput.value = '';
        // Refresh documents list
        fetchDocuments();
      } else {
        const errorData = await response.json();
        setUploadStatus(`Upload failed: ${errorData.detail || response.statusText}`);
      }
    } catch (error) {
      setUploadStatus(`Upload failed: ${error.message}`);
      console.error('Upload error:', error);
    }
  };

  // Handle document deletion
  const handleDeleteDocument = async (documentId) => {
    if (!window.confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/delete/${documentId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        // Refresh documents list
        fetchDocuments();
      } else {
        console.error('Failed to delete document:', response.statusText);
      }
    } catch (error) {
      console.error('Error deleting document:', error);
    }
  };

  // Handle reindexing all documents
  const handleReindex = async () => {
    if (!window.confirm('Are you sure you want to reindex all documents? This may take a while.')) {
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/reindex`, {
        method: 'POST',
      });

      if (response.ok) {
        alert('Reindexing started successfully!');
      } else {
        console.error('Failed to start reindexing:', response.statusText);
        alert('Reindexing failed!');
      }
    } catch (error) {
      console.error('Error starting reindexing:', error);
      alert('Reindexing failed!');
    }
  };

  // Load documents on component mount
  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div className="admin-panel">
      <h2>Document Management</h2>

      {/* Upload Section */}
      <div className="upload-section">
        <h3>Upload New Document</h3>
        <form onSubmit={handleFileUpload}>
          <div className="file-input-wrapper">
            <input
              id="file-upload"
              type="file"
              accept=".pdf,.doc,.docx,.txt,.md"
              onChange={(e) => setSelectedFile(e.target.files[0])}
            />
          </div>
          <button type="submit" disabled={!selectedFile}>
            Upload Document
          </button>
        </form>
        {uploadStatus && <div className="upload-status">{uploadStatus}</div>}
      </div>

      {/* Reindex Section */}
      <div className="reindex-section">
        <h3>Reindex Documents</h3>
        <button onClick={handleReindex} className="reindex-button">
          Reindex All Documents
        </button>
      </div>

      {/* Documents List */}
      <div className="documents-section">
        <h3>Uploaded Documents ({documents.length})</h3>
        {loading ? (
          <p>Loading documents...</p>
        ) : (
          <div className="documents-list">
            {documents.length > 0 ? (
              <table className="documents-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Filename</th>
                    <th>Size</th>
                    <th>Upload Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {documents.map((doc) => (
                    <tr key={doc.id}>
                      <td>{doc.id}</td>
                      <td>{doc.filename}</td>
                      <td>{doc.size ? `${(doc.size / 1024).toFixed(2)} KB` : 'N/A'}</td>
                      <td>{doc.upload_date || 'N/A'}</td>
                      <td>
                        <button
                          onClick={() => handleDeleteDocument(doc.id)}
                          className="delete-button"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No documents uploaded yet.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminPanel;