// ═══════════════════════════════════════
//  CADASTRO PET — Sprint 8
// ═══════════════════════════════════════

function updatePreview() {
  const nome  = document.getElementById('nome').value || 'Nome do pet';
  const esp   = document.getElementById('especie');
  const idade = document.getElementById('idade').value || '';
  const porte = document.getElementById('porte');

  const especieLabel = esp.options[esp.selectedIndex]?.text || 'Espécie';
  const porteLabel   = porte.options[porte.selectedIndex]?.text || 'Porte';

  document.getElementById('previewNome').textContent = nome;
  const meta = [especieLabel, idade, porteLabel].filter(Boolean).join(' · ');
  document.getElementById('previewMeta').textContent = meta || 'Espécie · Idade · Porte';
}

function updateEmojis() {
  const especie = document.getElementById('especie').value;
  ['cao', 'gato', 'outro'].forEach(e => {
    document.getElementById('emojis-' + e).style.display = 'none';
  });

  const hint = document.getElementById('emoji-hint-select');

  if (especie) {
    document.getElementById('emojis-' + especie).style.display = 'flex';
    hint.style.display = 'none';
    // Auto-seleciona primeiro emoji da espécie se nenhum selecionado
    const already = document.querySelector('.emoji-btn.selected');
    if (!already) {
      const first = document.querySelector('#emojis-' + especie + ' .emoji-btn');
      if (first) selectEmoji(first);
    }
  } else {
    hint.style.display = 'block';
  }
}

function selectEmoji(btn) {
  document.querySelectorAll('.emoji-btn').forEach(b => b.classList.remove('selected'));
  btn.classList.add('selected');
  const emoji = btn.dataset.emoji;
  document.getElementById('emojiInput').value = emoji;
  document.getElementById('previewEmoji').textContent = emoji;
}

// Restaura estado após POST com erro de validação
document.addEventListener('DOMContentLoaded', function () {
  const savedEmoji   = document.getElementById('emojiInput').value;
  const savedEspecie = document.getElementById('especie').value;

  if (savedEspecie) {
    updateEmojis();
    const savedBtn = document.querySelector(`.emoji-btn[data-emoji="${savedEmoji}"]`);
    if (savedBtn) selectEmoji(savedBtn);
  }

  if (savedEmoji) {
    document.getElementById('previewEmoji').textContent = savedEmoji;
  }

  updatePreview();
});
