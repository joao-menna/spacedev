async function getChat() {
    var res = await fetch("http://localhost:8090/api/chat", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: "olá ollama, como vai" })
    });

    var reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
    var chunks = [];

    while (true) {
        const { value, done } = await reader.read();
        if (done) {
            console.log(chunks);
            return chunks;
        }
        chunks.push(value)
        console.log(value)
    }
}

getChat()