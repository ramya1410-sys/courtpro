import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [form, setForm] = useState({
    case_type: "",
    case_number: "",
    filing_year: "",
    captcha_input: ""
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const fetchData = async () => {
    try {
      setLoading(true);
      const res = await axios.post("http://localhost:8000/api/fetch-case/", form);
      setResult(res.data);
    } catch {
      setResult({ error: "Could not fetch case data." });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{backgroundColor:"#E1E9C9", height: "100vh"}}>
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h2 style={{color:"#EDA35A",textAlign:"center"}}>Delhi High Court Case Lookup</h2>

      <p >
        🔐 Please open{" "}
        <a href="https://dhccaseinfo.nic.in/pcase/guiCaseWise.php" target="_blank" rel="noreferrer">
          Delhi HC Website
        </a>{" "}
        and copy the CAPTCHA code shown there.
      </p>

      <input name="case_type" placeholder="Case Type" onChange={handleChange} /><br />
      <input name="case_number" placeholder="Case Number" onChange={handleChange} /><br />
      <input name="filing_year" placeholder="Filing Year" onChange={handleChange} /><br />

      <input name="captcha_input" placeholder="Enter CAPTCHA from site" onChange={handleChange} /><br />

      <button
        onClick={fetchData}
        disabled={loading || !form.captcha_input}
        style={{ marginTop: "1rem" }}
      >
        {loading ? "Fetching..." : "Fetch Case"}
      </button>

      {result && (
        <div style={{ marginTop: "2rem" }}>
          {result.error ? (
            <p style={{ color: "red" }}>{result.error}</p>
          ) : (
            <>
              <p><strong>Parties:</strong> {result.party_names}</p>
              <p><strong>Filing Date:</strong> {result.filing_date}</p>
              <p><strong>Next Hearing:</strong> {result.next_hearing}</p>
              {result.latest_order_pdf && (
                <a href={result.latest_order_pdf} target="_blank" rel="noreferrer">
                  Download Latest Order
                </a>
              )}
            </>
          )}
        </div>
      )}
    </div>
    </div>
  );
}

export default App;
