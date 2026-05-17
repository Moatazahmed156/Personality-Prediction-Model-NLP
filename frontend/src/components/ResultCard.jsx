export default function ResultCard({ result }) {
  if (!result) return null;

  return (
    <div className="mt-6 p-4 border rounded-lg shadow-md bg-white">
      <h2 className="text-xl font-bold">
        {result.mbti_type} - {result.name}
      </h2>
      <p className="mt-2 text-gray-600">{result.description}</p>
      <p className="mt-2 font-semibold text-green-600">
        Confidence: {result.confidence}
      </p>
    </div>
  );
}