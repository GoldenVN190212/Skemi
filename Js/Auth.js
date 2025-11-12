// ================= FIREBASE IMPORT =================
import { auth, db } from "./Firebase_config.js";
import { 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword 
} from "https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js";
import { 
  setDoc, 
  doc, 
  getDoc 
} from "https://www.gstatic.com/firebasejs/11.0.1/firebase-firestore.js";

// =================== HÀM KIỂM TRA ===================
function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// =================== DOM EVENTS ===================
document.addEventListener("DOMContentLoaded", () => {

  // --- ĐĂNG KÝ ---
  const signupForm = document.getElementById("registerForm");
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = document.getElementById("signupUsername").value.trim();
      const email = document.getElementById("signupEmail").value.trim();
      const password = document.getElementById("signupPassword").value;
      const confirmPassword = document.getElementById("confirmPassword").value;

      if (!isValidEmail(email)) {
        alert("⚠️ Email không hợp lệ!");
        return;
      }

      if (password !== confirmPassword) {
        alert("⚠️ Mật khẩu xác nhận không khớp!");
        return;
      }

      try {
        // Tạo tài khoản mới
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        // Lưu thông tin vào Firestore
        await setDoc(doc(db, "users", user.uid), {
          email: email,
          username: username,
          createdAt: new Date()
        });

        alert("✅ Đăng ký thành công!");
        window.location.href = "Home.html"; // Chuyển sang trang chính
      } catch (error) {
        console.error("Chi tiết lỗi:", error);
        alert(`❌ Lỗi đăng ký: ${error.code} - ${error.message}`);
      }
    });
  }

  // --- ĐĂNG NHẬP ---
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const username = document.getElementById("loginUsername")?.value.trim();
      const email = document.getElementById("loginEmail").value.trim();
      const password = document.getElementById("loginPassword").value;

      try {
        // Đăng nhập
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;

        // Lấy dữ liệu Firestore để so username (nếu có trường username)
        const userDoc = await getDoc(doc(db, "users", user.uid));
        if (userDoc.exists()) {
          const data = userDoc.data();
          if (username && data.username !== username) {
            alert("⚠️ Sai username!");
            return;
          }
        }

        alert("✅ Đăng nhập thành công!");
        window.location.href = "Home.html"; // Chuyển sang trang chính
      } catch (error) {
        console.error("Chi tiết lỗi:", error);
        alert(`❌ Lỗi đăng nhập: ${error.code} - ${error.message}`);
      }
    });
  }
});
