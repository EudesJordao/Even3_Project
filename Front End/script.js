async function sendMessage() {
  const input = document.getElementById('user-input');
  const chatWindow = document.getElementById('chat-window');
  const userText = input.value.trim();

  if (!userText) return;

  input.value = '';


  // Mostra a mensagem do usuário no chat
  chatWindow.innerHTML += `<div class="chat-message user">${userText}</div>`;
  chatWindow.scrollTop = chatWindow.scrollHeight;

  try {
    const res = await fetch(`${window.API_BASE_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userText })  // <-- nome correto do campo
    });

    if (!res.ok) throw new Error(`Erro ${res.status}`);
    const json = await res.json();

    const botResponse = json.response || "Sem resposta do servidor.";
    setTimeout(() => {
      chatWindow.innerHTML += `<div class="chat-message bot">${botResponse}</div>`;
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }, 300);

  } catch (err) {
    console.error(err);
    chatWindow.innerHTML += `<div class="chat-message bot">Erro de comunicação com o servidor.</div>`;
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }

}