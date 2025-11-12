<<<<<<< HEAD
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
=======
// ================= FIREBASE INIT =================
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.0.1/firebase-app.js";
import { 
  getAuth, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword 
} from "https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js";

// 🔥 Thêm cấu hình Firebase của cậu chủ tại đây:
const firebaseConfig = {
  apiKey: "AIzaSyBYAgeL5xl2yfKMcmgiln5etyy-I-fvot0",
  authDomain: "skemivn.firebaseapp.com",
  projectId: "skemivn",
  storageBucket: "skemivn.firebasestorage.app",
  messagingSenderId: "430145480951",
  appId: "1:430145480951:web:dd640a426315a19aadcbf2"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// ================= ĐĂNG KÝ =================
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
      alert("⚠️ Mật khẩu xác nhận không khớp!");
      return;
    }

    try {
      await createUserWithEmailAndPassword(auth, email, password);
      alert("✅ Tạo tài khoản thành công!");
      window.location.href = "Home.html";
    } catch (error) {
      alert("❌ Lỗi: " + error.message);
    }
  });
}

// ================= ĐĂNG NHẬP =================
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("loginUsername").value.trim();
    const password = document.getElementById("loginPassword").value;

    try {
      await signInWithEmailAndPassword(auth, email, password);
      alert("✅ Đăng nhập thành công!");
      window.location.href = "Home.html"; // Trang chính Skemi
    } catch (error) {
      alert("❌ Lỗi: " + error.message);
    }
  });
}

export { app }; 
>>>>>>> b98baf73827f3d8b6b2220630551e2b28c5e01cc
