const { useState, useEffect } = React;

function App(){
    const [randomPost, setRandomPost] = useState('');

    const handleButtonClicl = () => {
        fetch('http://127.0.0.1:8000/product/')
            .then(response => response.json())
            .then(data => {
                const randomIndex = Math.floor(Math.random() * data.length);
                var post = data[randomIndex].title;
                setRandomPost(post);
            })
    }

    return (
        <div>
            <button onClick={handleButtonClicl}>Get Random Post</button>
            <div>{randomPost}</div>
        </div>
    )
}

var elem = document.getElementById('app');
ReactDOM.render(<App />, elem);
