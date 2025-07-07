import React from "react";
import "../home.css";

const Home = () => {
  return (
    <div>
      <div className="header">
        <ul>
          <li>
            <a href="/">WISEBUCKS.AI</a>
          </li>
          <div className="dropdown">
            <li>
              <a href="#">Features ▾</a>
            </li>
            <div className="dropdown-content">
              <a href="/chatbot">WiseBucks Chatbot</a>
              <a href="/investment">Investment Challenge</a>
              <a href="#">Reward Base Investing</a>
              <a href="/trading">Paper Trading</a>
            </div>
          </div>
          <li>
            <a href="#">About Us</a>
          </li>
          <li style={{ paddingRight: 570 }}>
            <a href="#">Contact Us</a>
          </li>
          <li>
            <a href="/login">Login</a>
          </li>
          <li>
            <a
              href="/signup"
              style={{
                backgroundColor: "white",
                color: "#003260",
                borderRadius: 5,
              }}
            >
              Sign Up
            </a>
          </li>
        </ul>
        <h4>Welcome to</h4>
        <h2>WiseBucks.AI</h2>
        <p>The Personal Assistant For Your Investment Journey</p>
        <div className="custom-button-container">
          <a className="custom-button" href="/dashboard">
            GET STARTED
          </a>
        </div>
        <div className="login-container">
          <a className="login-button" href="/login">
            LOGIN
          </a>
        </div>
      </div>
      <div className="mission">
        <h1>OUR MISSION</h1>
        <h2>
          Transforming your investment journey with precision and simplicity
          through our integrated AI platform, delivering accurate insights and
          personalized education for an elevated retail investor experience.
        </h2>
        <div className="row">
          {[1, 2, 3].map((i) => (
            <div className="column" key={i}>
              <div className="image">
                <img src="/images/target.png" alt="target" />
              </div>
              <div className="image-text">
                {i === 1 && (
                  <>
                    <p>Seamless investment with</p>
                    <p>our integrated AI platform</p>
                  </>
                )}
                {i === 2 && (
                  <>
                    <p>Personalized insights for</p>
                    <p>accurate investment decisions</p>
                  </>
                )}
                {i === 3 && (
                  <>
                    <p>Elevate your experience</p>
                    <p>with comprehensive education</p>
                  </>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="chat-box">
        <h2>AI INTERGRATION</h2>
        <h1>WISEBUCK CHATBOX</h1>
        <h3></h3>
        <div className="chatbot-button-container">
          <a className="chatbot-button" href="/chatbot">
            EXPLORE CHATBOT
          </a>
        </div>
      </div>
      <div className="chat-box2">
        <h2>PEER TO PEER COMPETITION</h2>
        <h1>INVESTMENT CHALLENGE</h1>
        <h3></h3>
        <div className="chatbot2-button-container">
          <a className="chatbot2-button" href="#">
            EXPLORE CHALLENGE
          </a>
        </div>
      </div>
      <div className="chat-box">
        <h2></h2>
        <h1>REWARD BASE INVESTING</h1>
        <h3></h3>
        <div className="chatbot-button-container">
          <a className="chatbot-button" href="/investment">
            EXPLORE INVESTING
          </a>
        </div>
      </div>
      <div className="chat-box2">
        <h2></h2>
        <h1>PAPER TRADING</h1>
        <h3></h3>
        <div className="chatbot2-button-container">
          <a className="chatbot2-button" href="/trading">
            EXPLORE TRADING
          </a>
        </div>
      </div>
      <footer className="footer">
        <div className="footer-container">
          <div className="row">
            <div className="footer-col">
              <h4 style={{ marginBottom: 0, paddingBottom: 0, fontSize: 30 }}>
                LO
              </h4>
              <h4 style={{ marginTop: 0, paddingTop: 0, fontSize: 30 }}>GO</h4>
            </div>
            <div
              className="footer-col"
              style={{ borderRight: "1mm solid white" }}
            >
              <h4 style={{ fontSize: 24 }}>WiseBucks.AI</h4>
              <h6 style={{ color: "white", fontSize: 8 }}>
                <i className="fa-regular fa-copyright"></i>WiseBuck.Ai, 2023
              </h6>
              <ul>
                <li>
                  <a href=""></a>
                </li>
              </ul>
            </div>
            <div className="footer-col">
              <h4>Features</h4>
              <ul>
                <li>
                  <a href="/chatbot">Wisebuck Chatbot</a>
                </li>
                <li>
                  <a href="/investment">Investment Challenege</a>
                </li>
              </ul>
            </div>
            <div className="footer-col">
              <h4 style={{ color: "inherit" }}>.</h4>
              <ul>
                <li>
                  <a href="#">Reward Base Investing</a>
                </li>
                <li>
                  <a href="/trading">Paper Trading</a>
                </li>
              </ul>
            </div>
            <div className="footer-col">
              <h4>Follow Us</h4>
              <div className="socials">
                <a href="#">
                  <i
                    className="fab fa-instagram"
                    style={{
                      display: "inline-block",
                      color: "white",
                      height: 20,
                      width: 20,
                      margin: "0 10px 10px 0",
                      textAlign: "center",
                      lineHeight: "40px",
                    }}
                  ></i>
                </a>
                <a href="#">
                  <i
                    className="fab fa-facebook"
                    style={{
                      display: "inline-block",
                      color: "white",
                      height: 20,
                      width: 20,
                      margin: "0 10px 10px 0",
                      textAlign: "center",
                      lineHeight: "40px",
                    }}
                  ></i>
                </a>
                <a href="#">
                  <i
                    className="fab fa-twitter"
                    style={{
                      display: "inline-block",
                      color: "white",
                      height: 20,
                      width: 20,
                      margin: "0 10px 10px 0",
                      textAlign: "center",
                      lineHeight: "40px",
                    }}
                  ></i>
                </a>
              </div>
            </div>
            <div className="footer-col">
              <h4>Join the community</h4>
              <div className="socials">
                <a href="#" style={{ color: "white", textDecoration: "none" }}>
                  <i
                    className="fab fa-discord"
                    style={{
                      display: "inline-block",
                      color: "white",
                      height: 20,
                      width: 20,
                      margin: "0 10px 10px 0",
                      textAlign: "center",
                      lineHeight: "40px",
                    }}
                  ></i>
                  Learn to Grow
                </a>
              </div>
            </div>
            <div className="footer-col">
              <div className="footer-button-container">
                <h4 style={{ color: "inherit" }}>.</h4>
                <a className="footer-button" href="#">
                  Contact Us
                </a>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Home;
