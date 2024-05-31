document.addEventListener('DOMContentLoaded', function() {
    // Set the subtitle with the current date
    const subtitle = document.getElementById('subtitle');
    const today = new Date();
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    subtitle.textContent = `Actualités du ${today.toLocaleDateString('fr-FR', options)}`;

    // Fetch and display the summaries
    fetch('summaries.json')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('articles-container');
            data.forEach(article => {
                const card = document.createElement('div');
                card.className = 'card';

                const title = document.createElement('h2');
                const link = document.createElement('a');
                link.href = article.link;
                link.textContent = article.title || 'Résumé';
                link.target = '_blank';  // Ouvre le lien dans un nouvel onglet
                title.appendChild(link);

                const body = document.createElement('p');
                body.textContent = article.body;

                card.appendChild(title);
                card.appendChild(body);

                container.appendChild(card);
            });

            // Observer pour l'animation
            const observer = new IntersectionObserver(entries => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                    } else {
                        entry.target.classList.remove('visible');
                    }
                });
            }, { threshold: 0.1 }); // Ajustez le seuil selon vos besoins

            // Ciblez toutes les cartes pour l'observation
            const cards = document.querySelectorAll('.card');
            cards.forEach(card => {
                observer.observe(card);
            });
        })
        .catch(error => console.error('Erreur lors du chargement des données:', error));
});
