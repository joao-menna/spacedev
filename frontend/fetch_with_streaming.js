async function getChat() {
    var res = await fetch("http://localhost:8090/api/chat", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: "olá spacedev, como vai?", chat_id: "123qwe" })
    });

    var reader = res.body.pipeThrough(new TextDecoderStream()).getReader();
    var chunks = [];

    while (true) {
        const { value, done } = await reader.read();
        if (done) {
            console.log(chunks.join(""));
            return chunks;
        }
        chunks.push(value)
        console.log(value)
    }
}

getChat()