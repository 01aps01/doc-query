import React, { useState, useRef } from "react";
import "./App.css";

const BACKEND_URL = "https://docquery-backend-mysi.onrender.com";

function App() {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [messages, setMessages] = useState([]);
  const inputRef = useRef();
  const hiddenFileInput = useRef(); 

  const triggerUpload = () => hiddenFileInput.current.click();

  const goHome = () => {
    setPdfUrl(null);
    setMessages([]);
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPdfUrl(URL.createObjectURL(file));

    let formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${BACKEND_URL}/ingest`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    setMessages([
      {
        sender: "system",
        text: `PDF uploaded successfully (${data.chunks} chunks indexed)`,
      },
    ]);
  };

  const askQuestion = async () => {
    const question = inputRef.current.value.trim();
    if (!question) return;

    setMessages((prev) => [...prev, { sender: "user", text: question }]);
    inputRef.current.value = "";

    const res = await fetch(`${BACKEND_URL}/query?question=${encodeURIComponent(question)}`, {
      method: "POST",
    });

    const data = await res.json();

    setMessages((prev) => [...prev, { sender: "bot", text: data.answer }]);
  };

  return (
    <>
      <div className="navbar">
        <div className="logo" onClick={goHome} style={{ cursor: "pointer" }}>
          DocQuery
        </div>

        <button className="topUploadBtn" onClick={triggerUpload}>
          Upload PDF
        </button>

        <input
          type="file"
          accept="application/pdf"
          ref={hiddenFileInput}
          onChange={handleUpload}
          style={{ display: "none" }}
        />
      </div>

      {!pdfUrl && (
        <div className="landing">
          <h1 className="title">
            Chat with any <span>PDF</span>
          </h1>

          <p className="subtitle">
            Instantly upload a PDF and start asking questions.
          </p>

          <label className="uploadBox">
            <div className="uploadIcon">📄</div>
            <p>Click or drag your PDF here</p>

            <input
              type="file"
              accept="application/pdf"
              onChange={handleUpload}
            />
          </label>
        </div>
      )}

      {pdfUrl && (
        <div className="mainLayout">
          <div className="pdfPanel">
            <iframe src={pdfUrl} title="PDF Preview" className="pdfView"></iframe>
          </div>

          <div className="chatPanel">
            <div className="chatBox">
              {messages.map((msg, i) => (
                <div key={i} className={`msg ${msg.sender}`}>
                  {msg.text}
                </div>
              ))}
            </div>

            <div className="inputRow">
              <input
                ref={inputRef}
                placeholder="Ask anything..."
                onKeyPress={(e) => {
                  if (e.key === "Enter") askQuestion();
                }}
              />
              <button onClick={askQuestion}>Send</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default App;
