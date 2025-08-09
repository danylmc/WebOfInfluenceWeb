import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "./auth/AuthProvider";
import { sendPasswordResetEmail } from "firebase/auth";
import { auth } from "./firebase";
import './CandidateOverview.css';

export default function Settings() {
  const { user } = useAuth();
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();
  const email = user?.email ?? "";
  const name  = user?.displayName ?? "(no display name)";

  const sendReset = async () => {
    try {
      setMsg("");
      await sendPasswordResetEmail(auth, email);
      setMsg("Password reset email sent. Check your inbox.");
    } catch (e) {
      setMsg(e.message || "Could not send reset email.");
    }
  };

  const handleBackToHome = () => navigate('/home');

  return (
    <div className="page-wrapper">
      <div className="candidate-wrapper">
        <div className="candidate-inner">

          {/* Header Row with back button */}
          <div className="donations-header-row">
            <h2 className="donations-search-header">Account Settings</h2>
            <button onClick={handleBackToHome} className="home-button">
              ← Back to Home
            </button>
          </div>

          {/* Profile Info */}
          <section style={{ marginTop: 16 }}>
            <h3>Profile</h3>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Username:</strong> {name}</p>
          </section>

          {/* Password Reset */}
          <section style={{ marginTop: 24 }}>
            <h3>Password</h3>
            <p>To change your password, send a secure reset email to <strong>{email}</strong>.</p>
            <button onClick={sendReset} className="action-button search-button">
              Send password reset email
            </button>
            {msg && <p style={{ marginTop: 8 }}>{msg}</p>}
          </section>
        </div>
      </div>
    </div>
  );
}