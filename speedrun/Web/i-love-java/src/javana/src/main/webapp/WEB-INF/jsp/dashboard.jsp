<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- SweetAlert2 -->
  <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
  <div class="bg-white shadow-lg rounded-lg p-8 w-full max-w-md">
    <h2 class="text-2xl font-bold mb-6 text-center text-gray-800">Dashboard</h2>
    <form id="upForm" enctype="multipart/form-data" class="flex flex-col gap-4">
      <input type="file" name="invoiceFile" accept=".xml" 
        class="block w-full text-sm text-gray-700 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500" />
      <button class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded transition-colors">
        Upload XML
      </button>
    </form>
  </div>

  <script>
    const f = document.getElementById('upForm');
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      const fd = new FormData(f);

      try {
        const r = await fetch('/api/upload', { method: 'POST', body: fd });
        const text = await r.text();
        let msg = '';
        let success = false;

        try {
          const j = JSON.parse(text);
          if (j.ok) {
            success = true;
            msg = j.message || "Upload successful!";
          } else {
            msg = j.error || j.msg || j.message || "Upload failed.";
          }
        } catch {
          msg = text;
        }

        if (r.status === 401) {
          location.href = '/login';
          return;
        }

        if (success) {
          Swal.fire({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            icon: 'success',
            title: 'Success',
            text: msg
          });
        } else {
          Swal.fire({
            toast: true,
            position: 'top-end',
            showConfirmButton: false,
            icon: 'error',
            title: 'Error',
            text: 'Something went wrong while processing.'
          });
        }

      } catch (err) {
        Swal.fire({
          toast: true,
          position: 'top-end',
          showConfirmButton: false,
          icon: 'error',
          title: 'Error',
          text: 'Something went wrong while uploading.'
        });
      }
    });
  </script>
</body>
</html>
