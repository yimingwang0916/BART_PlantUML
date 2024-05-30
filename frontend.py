import React, { useState } from "react";

function App() {
  const [description, setDescription] = useState("");
  const [plantuml, setPlantuml] = useState("");

  const generateDiagram = async () => {
    const response = await fetch("/generate/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ description }),
    });
    const data = await response.json();
    setPlantuml(data.plantuml);
  };

  return (
    <div>
      <h1>PlantUML Generator</h1>
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        rows="10"
        cols="50"
      ></textarea>
      <br />
      <button onClick={generateDiagram}>Generate</button>
      <pre>{plantuml}</pre>
    </div>
  );
}

export default App;
