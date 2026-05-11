function getCSRFToken() {
  return document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="))
    ?.split("=")[1];
}

function renderPosts(posts, isProfilePage = false) {
  const container = document.getElementById("posts-container");
  container.innerHTML = "";

  posts.forEach(post => {
    const div = document.createElement("div");
    div.classList.add("post-card");

    div.innerHTML = `
      <div><strong>${post.author_username}</strong></div>
      <div>${new Date(post.created_at).toLocaleString()}</div>
      <p>${post.content}</p>

      <strong>Likes: <span class="like-count">${post.like_count}</span></strong>
      <br><br>

      <button class="like-btn"
        data-id="${post.id}"
        data-liked="${post.liked_by_me}">
        ${post.liked_by_me ? "Unlike" : "Like"}
      </button>

      ${(isProfilePage || post.author === CURRENT_USER_ID) ? `
        <br><br>
        <button class="edit-btn" data-id="${post.id}">Edit</button>
        <button class="delete-btn" data-id="${post.id}">Delete</button>
      ` : ""}
    `;

    container.appendChild(div);
  });

  attachLikeHandlers();
  attachDeleteHandlers();
  attachEditHandlers();
}

function attachLikeHandlers() {
  document.querySelectorAll(".like-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const postId = btn.dataset.id;
      const liked = btn.dataset.liked === "true";

      const method = liked ? "DELETE" : "POST";
      const url = liked
        ? `/api/posts/${postId}/unlike/`
        : `/api/posts/${postId}/like/`;

      fetch(url, {
        method,
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": getCSRFToken()
        }
      })
      .then(() => {
        let countEl = btn.parentElement.querySelector(".like-count");
        let count = parseInt(countEl.innerText);

        if (liked) {
          count--;
          btn.innerText = "Like";
          btn.dataset.liked = "false";
        } else {
          count++;
          btn.innerText = "Unlike";
          btn.dataset.liked = "true";
        }

        countEl.innerText = count;
      });
    });
  });
}


function attachDeleteHandlers() {
  document.querySelectorAll(".delete-btn").forEach(btn => {
    btn.addEventListener("click", () => {

      const postId = btn.dataset.id;

      fetch(`/api/posts/${postId}/`, {
        method: "DELETE",
        credentials: "same-origin",
        headers: {
          "X-CSRFToken": getCSRFToken()
        }
      })
      .then(() => {
        btn.closest(".post-card").remove();
      });

    });
  });
}

function attachEditHandlers() {
  document.querySelectorAll(".edit-btn").forEach(btn => {

    btn.addEventListener("click", () => {

      const card = btn.closest(".post-card");
      const contentEl = card.querySelector("p");

      const originalText = contentEl.innerText;

      contentEl.innerHTML = `
        <textarea class="edit-area">${originalText}</textarea>
        <br>
        <button class="save-btn">Save</button>
      `;

      btn.style.display = "none";

      card.querySelector(".save-btn")
        .addEventListener("click", () => {

          const newContent =
            card.querySelector(".edit-area").value;

          const postId = btn.dataset.id;

          fetch(`/api/posts/${postId}/`, {
            method: "PATCH",
            credentials: "same-origin",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken()
            },
            body: JSON.stringify({ content: newContent })
          })
          .then(res => res.json())
          .then(updated => {

            contentEl.innerHTML = updated.content;
            btn.style.display = "inline";

          });

        });

    });

  });
}
function addPostToTop(post) {
  const container = document.getElementById('posts-container');
  container.innerHTML = "";

  const div = document.createElement("div");
  div.classList.add("post-card");

  div.innerHTML = `
    <strong>${post.author_username}</strong><br>
    <p>${post.content}</p>
    <small>${new Date(post.created_at).toLocaleString()}</small>
    <br>

    <strong>Likes: <span class="like-count">0</span></strong>
    <br><br>

    <button class="like-btn" data-id="${post.id}" data-liked="false">
      Like
    </button>

    <br><br>
    <button class="edit-btn" data-id="${post.id}">Edit</button>
    <button class="delete-btn" data-id="${post.id}">Delete</button>
  `;

  container.prepend(div);


  attachLikeHandlers();
  attachDeleteHandlers();
  attachEditHandlers();
}