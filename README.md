<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taş Kağıt Makas</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            color: white;
            transition: background 0.5s ease-in-out;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .choices button {
            font-size: 20px;
            margin: 10px;
            padding: 10px;
            border: none;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .choices button:hover {
            transform: scale(1.1);
        }
        #result, #score {
            font-size: 24px;
            margin-top: 20px;
            font-weight: bold;
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        #playButton {
            font-size: 22px;
            padding: 15px 30px;
            border: none;
            border-radius: 10px;
            background-color: #f1c40f;
            color: black;
            cursor: pointer;
            margin-bottom: 20px;
            transition: transform 0.2s;
        }
        #playButton:hover {
            transform: scale(1.1);
        }
        #game {
            display: none;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <button id="playButton" onclick="showGame()">Oyna</button>
        <div id="game">
            <h1>Taş Kağıt Makas</h1>
            <input type="text" id="team1" placeholder="1. Oyuncu Takım Adı">
            <input type="text" id="team2" placeholder="2. Oyuncu Takım Adı">
            <input type="number" id="rounds" placeholder="Kaç Tur Oynanacak?" min="1" value="3">
            <button onclick="startGame(1)" style="background-color: #3498db;">Tek Kişilik</button>
            <button onclick="startGame(2)" style="background-color: #e74c3c;">İki Kişilik</button>
            <p id="turn">Seçiminizi yapın:</p>
            <div class="choices">
                <button onclick="play('taş')">🪨 Taş</button>
                <button onclick="play('kağıt')">📄 Kağıt</button>
                <button onclick="play('makas')">✂️ Makas</button>
            </div>
            <p id="result"></p>
            <p id="score">Skor: 0 - 0</p>
        </div>
    </div>
    <script>
        let gameMode = 1;
        let player1Choice = "";
        let turn = 1;
        let player1Score = 0;
        let player2Score = 0;
        let rounds = 3;
        let currentRound = 0;

        function showGame() {
            document.getElementById("playButton").style.display = "none";
            document.getElementById("game").style.display = "block";
        }

        function startGame(mode) {
            gameMode = mode;
            document.getElementById("result").innerText = "";
            document.getElementById("turn").innerText = mode === 2 ? "1. Oyuncu seçimini yapıyor:" : "Seçiminizi yapın:";
            turn = 1;
            player1Choice = "";
            player1Score = 0;
            player2Score = 0;
            rounds = parseInt(document.getElementById("rounds").value);
            currentRound = 0;
            updateScore();
        }

        function play(choice) {
            if (gameMode === 1) {
                let choices = ["taş", "kağıt", "makas"];
                let computerChoice = choices[Math.floor(Math.random() * 3)];
                checkWinner(choice, computerChoice);
            } else {
                if (turn === 1) {
                    player1Choice = choice;
                    document.getElementById("turn").innerText = "2. Oyuncu seçimini yapıyor:";
                    turn = 2;
                } else {
                    checkWinner(player1Choice, choice);
                }
            }
        }

        function checkWinner(player1, player2) {
            let result = "";
            if (player1 === player2) {
                result = "Berabere!";
            } else if (
                (player1 === "taş" && player2 === "makas") ||
                (player1 === "kağıt" && player2 === "taş") ||
                (player1 === "makas" && player2 === "kağıt")
            ) {
                result = gameMode === 1 ? "Kazandınız!" : "1. Oyuncu Kazandı!";
                player1Score++;
            } else {
                result = gameMode === 1 ? "Bilgisayar Kazandı!" : "2. Oyuncu Kazandı!";
                player2Score++;
            }
            document.getElementById("result").innerText = `1. Oyuncu: ${player1} - 2. Oyuncu: ${player2}\n${result}`;
            document.body.style.background = result.includes("Kazandı") ? "linear-gradient(to right, #8e44ad, #3498db)" : "linear-gradient(to right, #c0392b, #e74c3c)";
            currentRound++;
            updateScore();
        }

        function updateScore() {
            document.getElementById("score").innerText = `Skor: ${player1Score} - ${player2Score}`;
            if (currentRound >= rounds) {
                document.getElementById("result").innerText += `\nOyun Bitti! ${player1Score > player2Score ? "1. Oyuncu Kazandı!" : player1Score < player2Score ? "2. Oyuncu Kazandı!" : "Berabere!"}`;
            }
        }
    </script>
</body>
</html>
