/*const opnSidebar = () => {
    document.getElementById("sidebar").style.width = "250px";
    document.getElementById("main").style.marginLeft = "250px";
};

const closeSidebar = () => {
    document.getElementById("sidebar").style.width = "0";
    document.getElementById("main").style.width = "0";
}; */


const sidebarHasItems = document.querySelectorAll('.has-child');
const subDropdownItems = document.querySelectorAll('.has-sub-child');

sidebarHasItems.forEach((item) =>{
    item.addEventListener('click', (e) => {
        e.preventDefault();

        const parentDropdown = item.closest('.has-dropdown');
        const isActivate = parentDropdown.classList.contains('active');

        const allDropdowns = document.querySelectorAll('.has-dropdown.active');
        allDropdowns.forEach((dropdown) =>{
            dropdown.classList.remove('active');
        });
        
        if(!isActivate){
            parentDropdown.classList.add('active');
        }
    });
});

subDropdownItems.forEach((item) => {
    item.addEventListener('click', (e)=>{
        e.preventDefault();
        
        const parentSubDropdown = item.closest('.has-sub-dropdown');
        const isActive = parentSubDropdown.classList.contains('active');

        const allSubDropdowns = document.querySelectorAll('.has-sub-dropdowns.active');
        allSubDropdowns.forEach((subDropdowns) => {
            subDropdowns.classList.remove('active');
        });
        
        if(!isActive){
            parentSubDropdown.classList.add('active');
        }
    });
});