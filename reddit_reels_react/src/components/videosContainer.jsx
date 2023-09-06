import React from 'react';
import VideoPlayer from './VideoPlayer';

const VideosContainer = (props) => {
    const { videoList } = props;

    return (
        <div>
          {videoList.map((video, index) => (
            <VideoPlayer key={index} videoUrl={`/videos/${video}`} />
          ))}
        </div>
      );
}

export default VideosContainer;