// Template Engine for Kali Teeri Wrapped
class WrappedRenderer {
  constructor(data, container) {
    this.data = data;
    this.container = container;
    this.swiper = null;
    this.currentSlideIndex = 0;
  }

  // Initialize Swiper and render cards
  init() {
    this.renderCards();
    this.initSwiper();
    this.addScrollIndicator();
    this.setupPagination();
    this.setupBackToTopButton();
    this.updateBackToTopButton(0);
  }

  // Render all cards based on their type
  renderCards() {
    this.data.forEach((card, index) => {
      const slide = document.createElement("div");
      slide.className = `swiper-slide theme-${card.theme.replace(
        "theme-",
        ""
      )}`;

      const cardHTML = this.renderCard(card, index);
      slide.innerHTML = cardHTML;

      this.container.appendChild(slide);
    });
  }

  // Template engine - routes to appropriate renderer based on card type
  renderCard(card, index) {
    switch (card.type) {
      case "intro":
        return this.renderIntroCard(card);
      case "ranked_list":
        return this.renderRankedListCard(card);
      case "big_highlight":
        return this.renderBigHighlightCard(card);
      case "comparison":
        return this.renderComparisonCard(card);
      default:
        return `<div class="card">Unknown card type: ${card.type}</div>`;
    }
  }

  // Render intro card template
  renderIntroCard(card) {
    return `
            <div class="card card-intro">
                <div class="card-suit">♠</div>
                <div class="title">${this.escapeHtml(card.title)}</div>
                <div class="subtitle">${this.escapeHtml(card.subtitle)}</div>
            </div>
        `;
  }

  // Unified helper function to create paginated pages
  createPaginatedPages(items, itemsPerPage, renderItemCallback) {
    const totalPages = Math.ceil(items.length / itemsPerPage);
    let pagesHTML = "";

    for (let page = 0; page < totalPages; page++) {
      const pageItems = items.slice(
        page * itemsPerPage,
        (page + 1) * itemsPerPage
      );
      const pageItemsHTML = pageItems
        .map((item, index) => {
          const globalIndex = page * itemsPerPage + index;
          return renderItemCallback(item, globalIndex, index);
        })
        .join("");

      const isFirstPage = page === 0;
      pagesHTML += `
        <div class="items-page ${
          isFirstPage ? "active" : ""
        }" data-page="${page}" style="${
        isFirstPage ? "display: flex;" : "display: none;"
      }">
          ${pageItemsHTML}
        </div>
      `;
    }

    return { pagesHTML, totalPages };
  }

  // Create pagination controls HTML
  createPaginationControls(cardId, totalPages) {
    if (totalPages <= 1) return "";

    return `
      <div class="pagination-controls" data-card-id="${cardId}">
        <button class="pagination-button pagination-prev" data-card-id="${cardId}" data-direction="prev" style="display: none;" aria-label="Previous page">
          Prev
        </button>
        <span class="page-indicator" data-card-id="${cardId}">1 / ${totalPages}</span>
        <button class="pagination-button pagination-next" data-card-id="${cardId}" data-direction="next" aria-label="Next page">
          Next
        </button>
      </div>
    `;
  }

  // Render ranked list card template
  renderRankedListCard(card) {
    const cardId = `ranked-${Date.now()}-${Math.random()
      .toString(36)
      .substr(2, 9)}`;

    const renderItem = (item, globalIndex, pageIndex) => {
      const rank = globalIndex + 1;
      return `
        <div class="ranked-item" data-rank="${rank}">
          <span class="rank">#${rank}</span>
          <span class="label">${this.escapeHtml(item.label)}</span>
          <span class="value">${this.escapeHtml(item.value)}</span>
        </div>
      `;
    };

    const { pagesHTML, totalPages } = this.createPaginatedPages(
      card.items,
      5,
      renderItem
    );

    const paginationControls = this.createPaginationControls(
      cardId,
      totalPages
    );

    const descriptionHTML = card.description
      ? `<div class="description">${this.escapeHtml(card.description)}</div>`
      : "";

    return `
      <div class="card card-ranked-list" data-card-id="${cardId}" data-current-page="0" data-total-pages="${totalPages}">
        <div class="title">${this.escapeHtml(card.title)}</div>
        ${descriptionHTML}
        <div class="items-viewport ranked-items-viewport">
          ${pagesHTML}
        </div>
        ${paginationControls}
      </div>
    `;
  }

  // Render big highlight card template
  renderBigHighlightCard(card) {
    // Check if extraPlayers exists for podium layout
    const hasExtraPlayers = card.extraPlayers && card.extraPlayers.length > 0;

    let extraPlayersHTML = "";
    if (hasExtraPlayers) {
      extraPlayersHTML = `
        <div class="podium-players">
          ${card.extraPlayers
            .map(
              (player, index) => `
            <div class="podium-player" data-rank="${index + 2}">
              <div class="podium-rank">#${index + 2}</div>
              <div class="podium-name">${this.escapeHtml(player.name)}</div>
              <div class="podium-stat">${this.escapeHtml(
                player.stat || player.value || ""
              )}</div>
            </div>
          `
            )
            .join("")}
        </div>
      `;
    }

    return `
            <div class="card card-big-highlight ${
              hasExtraPlayers ? "has-podium" : ""
            }">
                <div class="title">${this.escapeHtml(card.title)}</div>
                <div class="name">${this.escapeHtml(card.name)}</div>
                <div class="stat">${this.escapeHtml(card.stat)}</div>
                ${extraPlayersHTML}
                <div class="description">${this.escapeHtml(
                  card.description
                )}</div>
            </div>
        `;
  }

  // Render comparison card template
  renderComparisonCard(card) {
    const cardId = `comparison-${Date.now()}-${Math.random()
      .toString(36)
      .substr(2, 9)}`;

    const renderItem = (item, globalIndex, pageIndex) => {
      return `
        <div class="comparison-item">
          <div class="label">${this.escapeHtml(item.label)}</div>
          <div class="value">${this.escapeHtml(item.value)}</div>
        </div>
      `;
    };

    const { pagesHTML, totalPages } = this.createPaginatedPages(
      card.items,
      5,
      renderItem
    );

    const paginationControls = this.createPaginationControls(
      cardId,
      totalPages
    );

    return `
      <div class="card card-comparison" data-card-id="${cardId}" data-current-page="0" data-total-pages="${totalPages}">
        <div class="title">${this.escapeHtml(card.title)}</div>
        <div class="items-viewport comparison-items-viewport">
          ${pagesHTML}
        </div>
        ${paginationControls}
      </div>
    `;
  }

  // Initialize Swiper with vertical direction
  initSwiper() {
    this.swiper = new Swiper("#wrappedSwiper", {
      direction: "vertical",
      slidesPerView: 1,
      spaceBetween: 0,
      speed: 600,
      mousewheel: {
        enabled: true,
        sensitivity: 1,
      },
      touchEventsTarget: "container",
      keyboard: {
        enabled: true,
        onlyInViewport: false,
      },
      on: {
        slideChange: (swiper) => {
          this.onSlideChange(swiper.activeIndex);
        },
      },
    });
  }

  // Handle slide change events
  onSlideChange(newIndex) {
    this.currentSlideIndex = newIndex;
    // Hide scroll indicator after first slide
    if (newIndex > 0) {
      const scrollIndicator = document.querySelector(".scroll-indicator");
      if (scrollIndicator) {
        scrollIndicator.style.opacity = "0";
        scrollIndicator.style.pointerEvents = "none";
      }
    }
    // Show/hide back to top button
    this.updateBackToTopButton(newIndex);
  }

  // Update back to top button visibility
  updateBackToTopButton(currentIndex) {
    const backToTopBtn = document.getElementById("backToTop");
    if (backToTopBtn) {
      // Only show on the last slide (final "Game Over" card)
      const totalSlides = this.data.length;
      const isLastSlide = currentIndex === totalSlides - 1;

      if (isLastSlide) {
        backToTopBtn.classList.add("show");
      } else {
        backToTopBtn.classList.remove("show");
      }
    }
  }

  // Add scroll indicator to first slide
  addScrollIndicator() {
    // Wait for first slide to be rendered
    setTimeout(() => {
      const firstSlide = this.container.querySelector(
        ".swiper-slide:first-child"
      );
      if (firstSlide) {
        const indicator = document.createElement("div");
        indicator.className = "scroll-indicator";
        indicator.innerHTML = `
                    <div class="scroll-indicator-text">Swipe down</div>
                    <div class="scroll-indicator-arrow">↓</div>
                `;
        firstSlide.appendChild(indicator);
      }
    }, 100);
  }

  // Unified pagination handler for both ranked and comparison cards
  setupPagination() {
    document.addEventListener("click", (e) => {
      const button = e.target.closest(".pagination-button");
      if (!button) return;

      const cardId = button.getAttribute("data-card-id");
      const direction = button.getAttribute("data-direction");
      const card = document.querySelector(`[data-card-id="${cardId}"]`);

      if (!card) return;

      const currentPage = parseInt(card.getAttribute("data-current-page")) || 0;
      const totalPages = parseInt(card.getAttribute("data-total-pages")) || 1;

      // Validate direction
      if (
        (direction === "next" && currentPage >= totalPages - 1) ||
        (direction === "prev" && currentPage <= 0)
      ) {
        return; // Can't go further
      }

      const newPage = direction === "next" ? currentPage + 1 : currentPage - 1;

      // Get all pages in the viewport
      const viewport = card.querySelector(".items-viewport");
      if (!viewport) return;

      const currentPageContainer = viewport.querySelector(
        `.items-page[data-page="${currentPage}"]`
      );
      const nextPageContainer = viewport.querySelector(
        `.items-page[data-page="${newPage}"]`
      );

      if (!currentPageContainer || !nextPageContainer) return;

      // Fade out current page
      currentPageContainer.classList.remove("active");
      currentPageContainer.classList.add("fade-out");

      // After fade-out, switch pages
      setTimeout(() => {
        // Hide current page completely (display: none)
        currentPageContainer.style.display = "none";
        currentPageContainer.classList.remove("fade-out", "active");

        // Show and fade in next page
        nextPageContainer.style.display = "flex";
        nextPageContainer.classList.add("active", "fade-in");

        // Update card state
        card.setAttribute("data-current-page", newPage);

        // Update buttons and indicator
        this.updatePaginationControls(card, newPage, totalPages);

        // Force Swiper to recalculate slide height
        if (this.swiper) {
          this.swiper.update();
        }
      }, 300); // Match CSS transition duration
    });
  }

  // Update pagination control buttons and indicator
  updatePaginationControls(card, currentPage, totalPages) {
    const prevButton = card.querySelector(".pagination-prev");
    const nextButton = card.querySelector(".pagination-next");
    const pageIndicator = card.querySelector(".page-indicator");

    if (prevButton) {
      prevButton.style.display = currentPage > 0 ? "block" : "none";
    }
    if (nextButton) {
      nextButton.style.display =
        currentPage < totalPages - 1 ? "block" : "none";
    }
    if (pageIndicator) {
      pageIndicator.textContent = `${currentPage + 1} / ${totalPages}`;
    }
  }

  // Setup back to top button
  setupBackToTopButton() {
    const backToTopBtn = document.getElementById("backToTop");
    if (backToTopBtn) {
      backToTopBtn.addEventListener("click", () => {
        if (this.swiper) {
          this.swiper.slideTo(0);
        }
      });
    }
  }

  // Escape HTML to prevent XSS
  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
}

// Initialize the app when DOM is ready
document.addEventListener("DOMContentLoaded", () => {
  const container = document.getElementById("swiperWrapper");

  if (typeof wrappedData !== "undefined" && container) {
    const renderer = new WrappedRenderer(wrappedData, container);
    renderer.init();
    // Store renderer globally for visibility change handler
    window.wrappedRenderer = renderer;
  } else {
    console.error("Wrapped data or container not found");
  }
});
