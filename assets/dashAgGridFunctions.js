var dagfuncs = window.dashAgGridFunctions = window.dashAgGridFunctions || {};

var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagfuncs.getDataPath = function (data) {
    return data.Category;
}

dagcomponentfuncs.StockLink = function (props) {
    return React.createElement(
        'a',
        {href: props.value,  target: '_blank',
            style: {
                display: 'flex',         // Use flexbox for alignment
                justifyContent: 'center', // Center horizontally
                alignItems: 'center',    // Center vertically
                height: '100%',          // Ensure the anchor takes the full height of the cell
                textDecoration: 'none',  // Optional: Remove underline
            },
        },
        React.createElement(window.dash_iconify.DashIconify, {
            icon: "noto:link",
        }),
    );
};

dagcomponentfuncs.DataLink = function (props) {
    return React.createElement(
        'a',
        {href: props.value,  target: '_blank',
            style: {
                display: 'flex',         // Use flexbox for alignment
                justifyContent: 'center', // Center horizontally
                alignItems: 'center',    // Center vertically
                height: '100%',          // Ensure the anchor takes the full height of the cell
                textDecoration: 'none',  // Optional: Remove underline
            },
        },
        React.createElement(window.dash_iconify.DashIconify, {
            icon: "bx:data",
        }),
    );
};

dagcomponentfuncs.CodeLink = function (props) {
    return React.createElement(
        'div',
        {
            style: {
                display: 'flex',         // Use flexbox for alignment
                justifyContent: 'center', // Center horizontally
                alignItems: 'center',    // Center vertically
                height: '100%',          // Ensure the container takes the full height of the cell
                textDecoration: 'none',  // Optional: No underline style
            },
        },
        React.createElement(window.dash_iconify.DashIconify, {
            icon: "solar:code-bold",
        }),
    );
};