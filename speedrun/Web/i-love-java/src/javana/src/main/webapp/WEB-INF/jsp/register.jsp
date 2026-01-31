<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Register</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- SweetAlert2 -->
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
  <div class="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
    <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">Register</h2>
    <form id="regForm" class="flex flex-col gap-4">
      <input name="username" placeholder="Username"
        class="block w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
      <input name="password" type="password" placeholder="Password"
        class="block w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500" />
      <button
        class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded transition-colors">
        Register
      </button>
    </form>

    <p class="mt-4 text-center text-sm text-gray-600">
      Already have an account?
      <a href="/login" class="text-blue-600 hover:underline">Login</a>
    </p>
  </div>

  <script>
    const f = document.getElementById('regForm');
    f.addEventListener('submit', async (e) => {
      e.preventDefault();

      try {
        const r = await fetch('/api/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: f.username.value.trim(),
            password: f.password.value.trim()
          })
        });

        const j = await r.json();

        if (j.ok) {
          // Success toast then redirect to login
          Swal.fire({
            toast: true,
            icon: 'success',
            title: 'Registration successful! Redirecting...',
            position: 'top-end',
            showConfirmButton: false,
            timer: 2000,
            timerProgressBar: true
          }).then(() => {
            location.href = '/login';
          });
          return;
        }

        const msg = j.error || j.message || "Registration failed.";
        Swal.fire({
          toast: true,
          icon: 'error',
          title: msg,
          position: 'top-end',
          showConfirmButton: false,
          timer: 2500,
          timerProgressBar: true
        });

      } catch (err) {
        Swal.fire({
          toast: true,
          icon: 'error',
          title: 'Something went wrong while registering.',
          position: 'top-end',
          showConfirmButton: false,
          timer: 2500,
          timerProgressBar: true
        });
      }
    });
  </script>
</body>
</html>
