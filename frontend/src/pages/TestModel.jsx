import { useState } from "react";
import { predictPersonality } from "../services/api";
import ResultCard from "../components/ResultCard";

export default function TestModel() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    if (!text) return alert("Enter some text");

    try {
      setLoading(true);
      const res = await predictPersonality(text);
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Error connecting to API");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10">
      <textarea
        className="w-full p-3 border rounded-lg"
        rows="5"
        placeholder="Enter your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button
        onClick={handlePredict}
        className="mt-4 w-full bg-blue-600 text-white p-3 rounded-lg"
      >
        {loading ? "Predicting..." : "Predict Personality"}
      </button>

      <ResultCard result={result} />
    </div>
  );
}