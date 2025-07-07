import React, { useState } from "react";
import "../chatbot.css";

const EXAMPLE_PROMPTS = [
  "What's the current price of AAPL stock?",
  "Give me an update on tech stocks.",
  "Provide insights on promising stocks.",
];

const Chatbot = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handlePromptClick = (prompt) => {
    setInput(prompt);
    // Optionally auto-send the prompt
    // handleSend();
  };

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { sender: "user", text: input }]);
    setInput("");
    // Here you would call your backend/chatbot API and add the bot's response to messages
  };

  const handleInputKeyDown = (e) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div>
      {/* Navbar with dashboard link and brand */}
      <nav className="navbar navbar-expand-md navbar-dark fixed-top customNav">
        <div className="container-fluid">
          <a href="/dashboard">
            <div className="dash">
              <img
                src="/images/dasharrow.png"
                className="dash-arrow"
                alt="arrow"
              />
              <img
                src="/images/dashicon.png"
                className="dash-icon"
                alt="icon"
              />
              <div className="dash-text">Dashboard</div>
            </div>
          </a>
          <a className="navbar-brand" href="/">
            WISEBUCKS.AI
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarCollapse"
            aria-controls="navbarCollapse"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarCollapse">
            <ul className="navbar-nav me-auto mb-2 mb-md-0"></ul>
          </div>
        </div>
      </nav>
      {/* Main content */}
      <main className="flex-shrink-0" style={{ marginTop: 120 }}>
        <div className="container w-100 p-0">
          <div id="list-group" className="list-group w-100">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`list-group-item ${
                  msg.sender === "user" ? "userResponse" : "chatResponse"
                }`}
              >
                <p>{msg.text}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="bottomSpace"></div>
      </main>
      {/* Input area with example prompts and tutorial */}
      <div className="input-area">
        <h5>EXAMPLE PROMPTS:</h5>
        <div className="container w-100 p-0 prompts-container">
          <div className="row prompts-row">
            {EXAMPLE_PROMPTS.map((prompt, i) => (
              <div className="col" key={i}>
                <div
                  className="p-3 prompt"
                  onClick={() => handlePromptClick(prompt)}
                >
                  {prompt}
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="input-group mb-3">
          <input
            type="text"
            className="form-control"
            id="chat-input"
            placeholder="Send a message"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleInputKeyDown}
          />
          <img
            src="/images/send.png"
            id="gpt-button"
            alt="Send"
            style={{ cursor: "pointer" }}
            onClick={handleSend}
          />
        </div>
        <div className="tutorial-text">
          <h6>Need help with the chatbot? Watch our tutorials:</h6>
          <a href="/tutorials">
            <h6 style={{ fontWeight: 700 }}>TUTORIALS</h6>
          </a>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
