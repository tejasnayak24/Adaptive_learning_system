import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import Footer from "../components/Footer";

function StudentLayout({ children }) {
  return (
    <div className="min-h-screen">

      <Navbar />

      <div className="flex">

        <Sidebar />

        <main className="flex-1 p-10 bg-gray-100 overflow-y-auto">
          {children}
        </main>

      </div>

      <Footer />

    </div>
  );
}

export default StudentLayout;