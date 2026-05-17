import { useState } from "react";
import { Sun, Moon } from "lucide-react";

export default function NLPFrontend() {
  const [darkMode, setDarkMode] = useState(true);
  const [input, setInput] = useState("");
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const examples = [
  "I feel like people don’t really say what they mean, there’s always something hidden underneath.",
  "I don’t like overcomplicating life — just enjoy it.",
  "Rules are interesting only when you figure out how to bend them creatively.",
  "I often get lost thinking about theoretical possibilities that may never happen.",
  "I prefer taking charge because most groups lack direction.",
  "I can’t support something that goes against what I believe, even if everyone agrees with it.",
  "If something is not organized properly, it will eventually fail.",
  "I enjoy situations where I have to think fast under pressure.",
  "I love meeting new people and hearing their perspectives.",
  "I don’t need many people around me, but I need depth in the ones I choose.",
  "Execution matters more than ideas — ideas are cheap.",
  "I keep questioning how things actually work instead of just accepting explanations.",
  "Life feels like a story full of possibilities waiting to happen.",
  "I naturally notice when someone is upset even if they don’t say it.",
  "What if everything we consider normal is actually just a social illusion?",
  "I prefer planning everything in advance rather than reacting in the moment.",
  "I express myself more through actions than words.",
  "I get excited about too many things at once and want to try everything.",
  "Most people fail because they optimize for comfort instead of long-term results.",
  "I don’t overthink — I just act and deal with consequences later."
];
  // 🔗 Replace this URL with your real NLP backend API (FastAPI / Flask)
  const API_URL = "http://127.0.0.1:5000/predict";

  const handleRun = async () => {
    if (!input) return;

    setLoading(true);
    setResult("");

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: input }),
      });

      const data = await res.json();

      // expecting backend: { result: "...", confidence: 0.92 }
      setResult(
`🧠 Result: ${data.mbti_type}
📊 Confidence: ${(data.confidence)}
👤 Name: ${data.name}
📝 Description: ${data.description}`      );
    } catch (err) {
      setResult("❌ Error connecting to NLP API");
    }

    setLoading(false);
  };

  const handleExample = (text) => setInput(text);

  return (
    <div className={darkMode ? "dark" : ""}>
      <div className="min-h-screen transition-all duration-300 bg-gradient-to-br from-gray-950 via-gray-900 to-black text-white">

        {/* Header */}
        <div className="flex justify-between items-center p-5 bg-gray-900/70 backdrop-blur-md shadow-lg border-b border-purple-500/30">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-400 bg-clip-text text-transparent">
            NLP Intelligence Dashboard
          </h1>
        </div>

        {/* Main */}
        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">

          {/* Input */}
          <div className="bg-gray-900/60 border border-purple-500/20 p-5 rounded-2xl shadow-xl backdrop-blur-md">
            <h2 className="text-lg font-semibold mb-3 text-purple-300">Input Text</h2>

            <textarea
              className="w-full p-3 rounded-lg bg-gray-800 text-white outline-none focus:ring-2 focus:ring-purple-500"
              rows="6"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your NLP task..."
            />

            <button
              onClick={handleRun}
              disabled={loading}
              className="mt-4 w-full py-2 rounded-lg font-semibold bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500 hover:opacity-90 transition"
            >
              {loading ? "Processing..." : "Run NLP Model"}
            </button>
          </div>

          {/* Output */}
          <div className="bg-gray-900/60 border border-cyan-500/20 p-5 rounded-2xl shadow-xl backdrop-blur-md">
            <h2 className="text-lg font-semibold mb-3 text-cyan-300">AI Output</h2>

            <div className="p-3 min-h-[120px] bg-gray-800 rounded-lg whitespace-pre-wrap">
              {result || "Results will appear here..."}
            </div>
          </div>
        </div>

        {/* Examples */}
        <div className="p-6">
          <h2 className="text-xl font-bold mb-3 text-pink-400">Try Examples</h2>

          <div className="grid gap-3">
            {examples.map((ex, i) => (
              <button
                key={i}
                onClick={() => handleExample(ex)}
                className="text-left p-3 rounded-xl bg-gray-900/60 border border-purple-500/20 hover:border-pink-500 transition hover:scale-[1.01]"
              >
                {ex}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}