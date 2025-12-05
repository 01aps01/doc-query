import React, { useState, useRef } from "react";
import "./App.css";

function App() {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [messages, setMessages] = useState([]);
  const inputRef = useRef();
  const hiddenFileInput = useRef(); // for upload button

  // Trigger hidden input
  const triggerUpload = () => hiddenFileInput.current.click();

  // Go to home page
  const goHome = () => {
    setPdfUrl(null);
    setMessages([]);
  };

  // Upload PDF
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPdfUrl(URL.createObjectURL(file)); // show preview

    let formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/ingest", {
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

  // Ask question
  const askQuestion = async () => {
    const question = inputRef.current.value.trim();
    if (!question) return;

    setMessages((prev) => [...prev, { sender: "user", text: question }]);
    inputRef.current.value = "";

    const res = await fetch(
      `http://127.0.0.1:8000/query?question=${encodeURIComponent(question)}`,
      { method: "POST" }
    );

    const data = await res.json();
    setMessages((prev) => [...prev, { sender: "bot", text: data.answer }]);
  };

  return (
    <>
      {/* Top Navigation Bar */}
      <div className="navbar">
        <div className="logo" onClick={goHome} style={{ cursor: "pointer" }}>
          DocQuery
        </div>

        <button className="topUploadBtn" onClick={triggerUpload}>
          Upload PDF
        </button>

        {/* Hidden File Input */}
        <input
          type="file"
          accept="application/pdf"
          ref={hiddenFileInput}
          onChange={handleUpload}
          style={{ display: "none" }}
        />
      </div>

      {/* LANDING PAGE */}
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

            {/* Real file input */}
            <input
              type="file"
              accept="application/pdf"
              onChange={handleUpload}
            />
          </label>
        </div>
      )}

      {/* CHAT PAGE */}
      {pdfUrl && (
        <div className="mainLayout">
          {/* LEFT PDF PANEL */}
          <div className="pdfPanel">
            <iframe src={pdfUrl} title="PDF Preview" className="pdfView"></iframe>
          </div>

          {/* RIGHT CHAT PANEL */}
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
                  if (e.key === 'Enter') {
                    askQuestion();
                  }
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
