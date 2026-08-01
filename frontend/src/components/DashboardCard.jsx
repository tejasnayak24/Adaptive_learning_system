function DashboardCard({ title, value, description }) {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition">
      <h2 className="text-lg font-semibold text-gray-700">{title}</h2>

      <p className="text-3xl font-bold text-blue-600 mt-3">
        {value}
      </p>

      <p className="text-gray-500 mt-2">
        {description}
      </p>
    </div>
  );
}

export default DashboardCard;