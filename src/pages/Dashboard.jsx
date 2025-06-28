import React from 'react';
import { useNavigate } from 'react-router-dom';

const LoanCard = ({ title, description, navigateTo }) => {
  const navigate = useNavigate();
  return (
    <div className="bg-white rounded-lg shadow-md p-6 flex flex-col items-center text-center">
      <h3 className="text-xl font-semibold mb-3 text-gray-800">{title}</h3>
      <p className="text-gray-600 mb-5">{description}</p>
      <button
        onClick={() => navigate(navigateTo)}
        className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg focus:outline-none focus:shadow-outline transition duration-200 cursor-pointer"
      >
        Apply
      </button>
    </div>
  );
};

const Dashboard = ({ setIsLoggedIn }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    setIsLoggedIn(false); // Clear login state
    navigate('/login'); // Redirect to login
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navbar */}
      <nav className="bg-blue-800 text-white p-4 shadow-md">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center">
            <div className="w-8 h-8 mr-2 bg-white rounded-full flex items-center justify-center text-blue-800 font-bold">M</div>
            <span className="text-xl font-bold">Loan System</span>
          </div>
          {/* <div>
            <span className="mr-4 hidden sm:inline">Hello, Ayra</span>
            <a href="#" className="mr-4 hover:underline hidden sm:inline">Regulations</a>
            <a href="#" className="mr-4 hover:underline hidden sm:inline">Suggestions</a>
            <button
              onClick={handleLogout}
              className="bg-red-500 hover:bg-red-600 text-white font-semibold py-1 px-4 rounded-md transition duration-200"
            >
              Logout
            </button>
          </div> */}
        </div>
      </nav>

      {/* Main Content */}
      <div className="container mx-auto p-8 mt-8">
        <h2 className="text-2xl font-bold mb-8 text-gray-800">Welcome to Your Loan Dashboard</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <LoanCard
            title="Loans within Savings"
            description="Access funds directly from your savings with competitive rates."
            navigateTo="/apply/savings-loan"
          />
          <LoanCard
            title="Loans Above Savings"
            description="Need more? Apply for loans exceeding your current savings."
            navigateTo="/apply/above-savings-loan"
          />
          <LoanCard
            title="Loans Covered by Salary"
            description="Get a loan secured by your regular salary. Quick and easy."
            navigateTo="/apply/salary-loan"
          />
          <LoanCard
            title="Loans Covered by Standing Order"
            description="Automate repayments with a standing order for convenience."
            navigateTo="/apply/standing-order-loan"
          />
          <LoanCard
            title="Mortgage Loans"
            description="Dream big with our flexible mortgage solutions for your home."
            navigateTo="/apply/mortgage-loan"
          />
          {/* Add more loan types as needed */}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;