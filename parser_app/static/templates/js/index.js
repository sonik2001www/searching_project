// animation onload
const navbarAnimation = document.querySelector(".navbar-animation");
const bodyAnimation = document.querySelector(".opacity-animation");
document.body.onload = () => {
  if (navbar) {
    navbar.classList.remove("navbar-animation");
  }
  if (bodyAnimation) {
    bodyAnimation.classList.remove("opacity-animation");
  }
};

// small navbar
const navbar = document.getElementById("navbar");
const navbar_content = document.getElementById("navbar-content");
const containers = document.querySelectorAll(".container");

const toggleSmallNavbar = () => {
  navbar.classList.toggle("small-navbar");

  containers.forEach((container) => {
    container.classList.toggle("small-navbar-container");
  });
};

if (navbar_content) {
  navbar_content.addEventListener("click", (e) => {
    e.stopPropagation();
  });
}

// mobile navbar
const burger = document.querySelector(".burger");
if (burger) {
  burger.addEventListener("click", () => {
    navbar.classList.add("navbar-isActive");
    burger.classList.add("burger-isActive");
    document.body.classList.add("no-scroll");

    let paddingScroll = window.innerWidth - document.body.offsetWidth + "px";
    document.body.style.paddingRight = paddingScroll;
  });
}

// close navbar
const closeNavbarBtn = document.querySelector(".navbar-close");

const closeNavbar = () => {
  navbar.classList.remove("navbar-isActive");
  burger.classList.remove("burger-isActive");
  document.body.style.paddingRight = 0;
  document.body.classList.remove("no-scroll");
};
if (closeNavbarBtn && burger) {
  closeNavbarBtn.addEventListener("click", closeNavbar);
}

// close navbar on click out
const closeNavbarClickOut = (e) => {
  const clickBurger = e.composedPath().includes(burger);
  const clickNavbar = e.composedPath().includes(navbar);

  if (clickBurger) {
    return;
  } else if (!clickNavbar) {
    closeNavbar();
  }
};

// Search result close
const form_search = document.querySelectorAll(".search__input");

const searchResult = () => {
  form_search.forEach((el) => {
    const search_results = el.querySelectorAll(".search__result");
    const search = el.querySelector(".search__field");

    search_results.forEach((search_result) => {
      searchCloseBtn = search_result.querySelector(".search__result-close");

      searchCloseBtn.addEventListener("click", () => {
        search_result.remove();

        // show placeholder if len result = 0
        if (el.querySelectorAll(".search__result").length === 0) {
          search.placeholder = "Search";
          search.classList.remove("no-pointer-events");
          el.classList.remove(".input-border");
        }
      });
    });

    // add style if have resault
    if (el.querySelectorAll(".search__result").length !== 0) {
      search.placeholder = "";
      search.classList.add("no-pointer-events");
      el.classList.add("input-border");
    } else {
      search.placeholder = "Search";
    }
  });
};

if (form_search) {
  searchResult();
}

// ACARDEONS
const acarddeons = document.querySelectorAll(".acarddeon");

const initAcarddeon = () => {
  acarddeons.forEach((acarddeon) => {
    const acarddeon_toggler = acarddeon.querySelector(".acarddeon__toggler");
    const acarddeon_body = acarddeon.querySelector(".acarddeon__body");

    const removeStylesAcardeon = () => {
      document
        .querySelectorAll(".acarddeon__body")
        .forEach((el) => (el.style.maxHeight = null));
      document
        .querySelectorAll(".acarddeon__toggler")
        .forEach((el) => el.classList.remove("acarddeon__toggler-isActive"));
    };

    const onClickToogler = () => {
      if (acarddeon_body.style.maxHeight) {
        removeStylesAcardeon();
      } else {
        removeStylesAcardeon();
        acarddeon_body.style.maxHeight = acarddeon_body.scrollHeight + "rem";
        acarddeon_toggler.classList.add("acarddeon__toggler-isActive");
      }
    };
    acarddeon_toggler.addEventListener("click", onClickToogler);
  });
};

if (acarddeons) {
  initAcarddeon();
}

// sort
const sortBts = document.querySelectorAll(".styled-table th");

const initSort = () => {
  sortBts.forEach((sortBtn) => {
    const classListBtn = sortBtn.classList;

    sortBtn.addEventListener("click", () => {
      if (classListBtn.contains("sort-first")) {
        sortBts.forEach((el) => (el.classList = null));

        classListBtn.remove("sort-first");
        classListBtn.add("sort-second");
      } else if (classListBtn.contains("sort-second")) {
        sortBts.forEach((el) => (el.classList = null));

        classListBtn.remove("sort-second");
        classListBtn.add("sort-first");
      } else {
        sortBts.forEach((el) => (el.classList = null));

        classListBtn.add("sort-first");
      }
    });
  });
};

if (sortBts) {
  initSort();
}

const password = document.getElementById("password");
const show_password = document.querySelector(".show-password");

if (show_password) {
  show_password.addEventListener("click", () => {
    const type = password.type;

    if (type === "password") {
      password.type = "text";
      show_password.classList.add("show-password-isActive");
    } else {
      password.type = "password";
      show_password.classList.remove("show-password-isActive");
    }
  });
}

// media tablet
const tablet_breakpoint = "1100px";
const media_query_tablet = window.matchMedia(
  `(max-width: ${tablet_breakpoint})`
);

function toggle_tablet(e) {
  if (e.matches) {
    if (navbar) {
      navbar.removeEventListener("click", toggleSmallNavbar);
      navbar.classList.add("small-navbar");
    }

    containers.forEach((container) => {
      container.classList.add("small-navbar-container");
    });
  } else {
    if (navbar) {
      navbar.addEventListener("click", toggleSmallNavbar);
      navbar.classList.remove("small-navbar");
    }

    containers.forEach((container) => {
      container.classList.remove("small-navbar-container");
    });
  }
}
toggle_tablet(media_query_tablet);

media_query_tablet.addEventListener("change", toggle_tablet);

// media mobile
const mobile_breakpoint = "700px";
const media_query_mobile = window.matchMedia(
  `(max-width: ${mobile_breakpoint})`
);

function toggle_mobile(e) {
  if (e.matches) {
    if (navbar && burger) {
      navbar.classList.remove("small-navbar");
      document.body.addEventListener("click", closeNavbarClickOut);
    }

    containers.forEach((container) => {
      container.classList.remove("small-navbar-container");
    });
  } else {
    toggle_tablet(media_query_tablet);

    document.body.removeEventListener("click", closeNavbarClickOut);
  }
}
toggle_mobile(media_query_mobile);

media_query_mobile.addEventListener("change", toggle_mobile);

// dropmenu
const drops = document.querySelectorAll('[data-drop]');

if (drops.length) {
  initDropMenu();
}

function initDropMenu() {
  drops.forEach((dropWrapper) => {
    const dropMenu = dropWrapper.querySelector("[data-dropMenu]");
    const dropBtn = dropWrapper.querySelector("[data-dropBtn]");
    dropBtn.addEventListener("click", () => {
      if (dropMenu.classList.contains("active")) {
        dropMenu.classList.remove("active");
        dropBtn.classList.remove("active");
      } else {
        dropMenu.classList.add("active");
        dropBtn.classList.add("active");
      }
    });
    closeOnClickOut(dropMenu, dropBtn, dropWrapper);
  });

  function closeOnClickOut(dropMenu, dropBtn, dropWrapper){
    let firstBtnClassName = dropBtn.className.replace(/ [\s\S]+/, '');
    let firstMenuClassName = dropMenu.className.replace(/ [\s\S]+/, '');

    window.addEventListener("click", (e) => {
      if (dropMenu.classList.contains("active")) {
        let clickOnBtn = e.target.closest(`.${firstBtnClassName}`);
        let clickOnMenu = e.target.closest(`.${firstMenuClassName}`);

        if (!clickOnBtn && !clickOnMenu) {
          dropMenu.classList.remove("active");
          dropBtn.classList.remove("active");
        }
      }
    });
  };
}
// select
document.querySelectorAll('.dropdown').forEach(function (dropdownWrapper) {
  const dropdownBtn = dropdownWrapper.querySelector('.dropdown__button');
  const dropdownList = dropdownWrapper.querySelector('.dropdown__list');
  const dropdownItems = dropdownList.querySelectorAll('.dropdown__list-item');
  const dropdownInput = dropdownWrapper.querySelector('.dropdown__input_hidden')
  
  dropdownBtn.addEventListener('click', function () {
    dropdownList.classList.toggle('dropdown__list_visible');
    this.classList.toggle('dropdown__button_active');
  });
  
  dropdownItems.forEach(function(listItem) {
    listItem.addEventListener('click', function (e) {
      dropdownItems.forEach(function(el) {
        el.classList.remove('dropdown__list-item_active');
      })
      e.target.classList.add('dropdown__list-item_active');
      dropdownBtn.innerText = this.innerText;
      dropdownInput.value = this.dataset.value;
      dropdownList.classList.remove('dropdown__list_visible');
    })
  })
  
  document.addEventListener('click', function (e) {
    if ( e.target !== dropdownBtn ){
      dropdownBtn.classList.remove('dropdown__button_active');
      dropdownList.classList.remove('dropdown__list_visible');
    }
  })
  
  document.addEventListener('keydown', function (e) {
    if( e.key === 'Tab' || e.key === 'Escape' ) {
      dropdownBtn.classList.remove('dropdown__button_active');
      dropdownList.classList.remove('dropdown__list_visible');
    }
  }) 
})

document.querySelectorAll('.dropdown_with-chk').forEach(function (dropdownWrapper) {
  const dropdownBtn = dropdownWrapper.querySelector('.dropdown_with-chk__button');
  const dropdownList = dropdownWrapper.querySelector('.dropdown_with-chk__list');
  const dropdownItems = dropdownList.querySelectorAll('.dropdown_with-chk__list-item');
  
  dropdownBtn.addEventListener('click', function () {
    dropdownList.classList.toggle('dropdown_with-chk__list_visible');
    this.classList.toggle('dropdown_with-chk__button_active');
  });
  
  dropdownItems.forEach(function(listItem) {
    listItem.addEventListener('click', function (e) {
      e.target.classList.toggle('dropdown_with-chk__list-item_active');
    })
  })
  
  document.addEventListener('click', function (e) {
    if ( e.target !== dropdownBtn && e.target !== dropdownItems && !e.target.classList.contains('dropdown_with-chk__list-item') && !e.target.classList.contains('dropdown_with-chk__list-item_label')){
      dropdownBtn.classList.remove('dropdown_with-chk__button_active');
      dropdownList.classList.remove('dropdown_with-chk__list_visible');
    }
  })
  
  document.addEventListener('keydown', function (e) {
    if( e.key === 'Tab' || e.key === 'Escape' ) {
      dropdownBtn.classList.remove('dropdown_with-chk__button_active');
      dropdownList.classList.remove('dropdown_with-chk__list_visible');
    }
  }) 
})

//// remove filter
//const removeFilters = document.querySelectorAll('.remove-filter__menu')
//
//if (removeFilters.length){initFilterRemoveFun()}
//
//function initFilterRemoveFun(){
//  removeFilters.forEach((el) => {
//    const removeInput = el.querySelector('.remove-filter__input')
//    const removeBtn = el.querySelector('.add-remove')
//
//    removeInput.addEventListener('keyup', () => {
//    console.log(removeInput.value)
//      if (removeInput.value){
//        removeBtn.classList.remove('add-remove-disabled')
//      } else {
//        removeBtn.classList.add('add-remove-disabled')
//      }
//    })
//  })
//}
//
//// calendars
//const calendars = document.querySelectorAll('.add-deal__input-calendar')
//if (calendars.length){initCalendar()}
//
//function initCalendar() {
//
//  calendars.forEach((calendarWrapper) => {
//    const calendarBtn = calendarWrapper.querySelector('.add-deal__input-calendar-btn')
//    const calendar = calendarWrapper.querySelector('.calendar-box-container')
//
//    calendarBtn.addEventListener("click",  (e) => {
//      calendarBtn.classList.toggle('add-deal__input-calendar-btn-open')
//      calendar.classList.toggle('calendar-box-container-open')
//    });
//
//    hiideOnClickOut(calendarBtn, calendar)
//  })
//
//  function hiideOnClickOut(calendarBtn, calendar) {
//    document.addEventListener("click", (e) => {
//      if (!e.composedPath().includes(calendarBtn) && !e.composedPath().includes(calendar)){
//        calendarBtn.classList.remove('add-deal__input-calendar-btn-open')
//        calendar.classList.remove('calendar-box-container-open')
//      }
//    });
//  }
//
//}