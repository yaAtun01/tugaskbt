/**
 * MountainGo Bromo Trip - Client-side Script
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Navigation Toggle
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.getElementById('navLinks');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            
            // Toggle hamburger animation
            const spans = menuToggle.querySelectorAll('span');
            if (navLinks.classList.contains('active')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(6px, -6px)';
            } else {
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            }
        });
    }

    // 2. Pre-select Package from URL Query Param (jika ada)
    const selectPaket = document.getElementById('paket');
    if (selectPaket) {
        // Ambil query parameter dari URL
        const urlParams = new URLSearchParams(window.location.search);
        const paketParam = urlParams.get('paket');

        if (paketParam) {
            // Cocokkan nilai parameter dengan value option di dropdown
            for (let i = 0; i < selectPaket.options.length; i++) {
                if (selectPaket.options[i].value.toLowerCase() === paketParam.toLowerCase()) {
                    selectPaket.selectedIndex = i;
                    break;
                }
            }
        }
    }

    // 3. Menutup Modal Sukses
    const closeModalBtn = document.getElementById('closeModalBtn');
    const successModal = document.getElementById('successModal');

    if (closeModalBtn && successModal) {
        closeModalBtn.addEventListener('click', () => {
            successModal.style.display = 'none';
            // Bersihkan query string dari URL tanpa me-reload halaman
            const cleanUrl = window.location.protocol + "//" + window.location.host + window.location.pathname;
            window.history.replaceState({ path: cleanUrl }, '', cleanUrl);
        });
    }

    // 4. Konfirmasi Admin saat Mengubah Status
    const statusForms = document.querySelectorAll('.status-form');
    statusForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const selectElement = form.querySelector('.status-select');
            const selectedStatus = selectElement.options[selectElement.selectedIndex].text;
            const confirmMsg = `Apakah Anda yakin ingin mengubah status pemesanan ini menjadi "${selectedStatus}"?`;
            
            if (!confirm(confirmMsg)) {
                e.preventDefault(); // Batalkan submit jika tidak setuju
            }
        });
    });
});
