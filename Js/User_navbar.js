import { auth } from "./Firebase_config.js";
import { onAuthStateChanged, signOut } 
  from "https://www.gstatic.com/firebasejs/11.0.1/firebase-auth.js";

document.addEventListener("DOMContentLoaded", () => {
  const navbar = document.getElementById("navbar");
  const logout = document.getElementById("logoutBtn");

  onAuthStateChanged(auth, (user) => {
    if (!navbar) return;

    // Xóa nút cũ
    navbar.querySelectorAll("#signupBtn,#loginBtn,#userBtn").forEach(b => b.remove());

    if (!user) {
      navbar.innerHTML += `
        <button class="tab" id="signupBtn">Sign up</button>
        <button class="tab" id="loginBtn">Log in</button>
      `;
      if (logout) logout.style.display = "none";

      document.getElementById("signupBtn").onclick = () =>
        (window.location.href = "Register.html");
      document.getElementById("loginBtn").onclick = () =>
        (window.location.href = "Login.html");
    } else {
      const username = user.email.split("@")[0];
      const userBtn = document.createElement("button");
      userBtn.className = "tab user-btn";
      userBtn.id = "userBtn";
      userBtn.innerHTML = `🔒 ${username}`;
      console.log(`🔒 Đã đăng nhập với username: ${username}`);
      navbar.appendChild(userBtn);

      if (logout) {
        logout.style.display = "block";
        logout.onclick = async () => {
          await signOut(auth);
          window.location.href = "Login.html";
        };
      }
    }
  });
});
