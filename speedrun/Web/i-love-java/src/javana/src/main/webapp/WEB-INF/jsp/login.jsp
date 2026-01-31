<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Login</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- SweetAlert2 -->
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
  <div class="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
    <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">Login</h2>
    <form id="loginForm" class="flex flex-col gap-4">
      <input name="username" placeholder="Username"
        class="block w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
      <input name="password" type="password" placeholder="Password"
        class="block w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
      <button
        class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded transition-colors">
        Login
      </button>
    </form>
    <p class="mt-4 text-center text-sm text-gray-600">
      Don't have an account? 
      <a href="/register" class="text-blue-600 hover:underline">Register</a>
    </p>
  </div>

  <script>
    const f = document.getElementById('loginForm');
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      const body = JSON.stringify({
        username: f.username.value.trim(),
        password: f.password.value.trim()
      });

      try {
        const r = await fetch('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body
        });
        const j = await r.json();

        if (j.ok && j.redirect) {
          location.href = j.redirect;
          return;
        }

        const msg = j.error || j.message || "Login failed.";
        Swal.fire({
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          icon: 'error',
          title: 'Login Failed',
          text: msg
        });

      } catch (err) {
        Swal.fire({
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          icon: 'error',
          title: 'Error',
          text: 'Something went wrong while logging in.'
        });
      }
    });
  </script>
</body>
</html>
