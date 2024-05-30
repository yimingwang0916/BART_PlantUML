import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [description, setDescription] = useState("");
  const [plantuml, setPlantuml] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const generateDiagram = async () => {
    setLoading(true);
    setError("");
    try {
      const response = await axios.post("http://localhost:8000/generate/", {
        description,
      });
      setPlantuml(response.data.plantuml);
    } catch (err) {
      setError("Failed to generate PlantUML code.");
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>PlantUML Generator</h1>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows="10"
          cols="50"
          placeholder="Enter scenario description here..."
        ></textarea>
        <br />
        <button onClick={generateDiagram} disabled={loading}>
          {loading ? "Generating..." : "Generate"}
        </button>
        {error && <p className="error">{error}</p>}
        <pre className="plantuml-output">{plantuml}</pre>
      </header>
    </div>
  );
}

export default App;
