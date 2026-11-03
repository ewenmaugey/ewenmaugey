<!doctype html>
<html lang="fr">
<meta charset="utf-8">
<title>Égaliseur animé</title>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    min-height: 100vh;
    display: grid;
    place-items: center;
    background: #000;
  }
  .equalizer {
    height: 120px;
    display: flex;
    align-items: end;
    gap: 2px;
  }
  .bar {
    width: 7px;
    height: var(--height);
    background: var(--color);
    box-shadow: 0 0 7px var(--color);
    transform-origin: bottom;
    animation: pulse var(--speed) ease-in-out infinite alternate;
    animation-delay: var(--delay);
  }
  @keyframes pulse {
    from { transform: scaleY(.25); }
    to   { transform: scaleY(1); }
  }
</style>
<div class="equalizer" aria-label="Égaliseur coloré animé"></div>
<script>
  const heights = [14,20,28,38,50,42,62,74,55,86,64,48,72,58,94,112,78,58,40,28,42,34,24,18,28,22,16];
  const equalizer = document.querySelector(".equalizer");

  heights.forEach((height, i) => {
    const bar = document.createElement("div");
    const hue = 5 + (i / (heights.length - 1)) * 245;
    bar.className = "bar";
    bar.style.setProperty("--height", `${height}px`);
    bar.style.setProperty("--color", `hsl(${hue}, 100%, 50%)`);
    bar.style.setProperty("--speed", `${0.35 + Math.random() * 0.55}s`);
    bar.style.setProperty("--delay", `${Math.random() * -1.2}s`);
    equalizer.appendChild(bar);
  });
</script>
</html>
