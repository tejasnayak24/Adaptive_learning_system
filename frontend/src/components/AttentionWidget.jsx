function AttentionWidget() {
  const attention = 92;

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">

      <div className="flex items-center justify-between">

        <div>
          <h2 className="text-2xl font-semibold">
            👀 Attention Score
          </h2>

          <p className="text-gray-500 mt-1">
            Live concentration level
          </p>
        </div>

        <div className="text-4xl font-bold text-green-600">
          {attention}%
        </div>

      </div>

      <div className="mt-6">

        <div className="w-full bg-gray-200 rounded-full h-4">

          <div
            className="bg-green-500 h-4 rounded-full"
            style={{ width: `${attention}%` }}
          ></div>

        </div>

      </div>

      <p className="mt-4 text-green-600 font-semibold">
        Excellent Focus 🎯
      </p>

    </div>
  );
}

export default AttentionWidget;