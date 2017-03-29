
/* Set up shit that I barely understand */
var ISSChatApp = angular.module('ISSChatApp', []);

ISSChatApp.controller('ChatController', function($scope)
{
    
    var socket = io.connect('https://' + document.domain + ':8080');
   // +location.port + '/iss');
    
    $scope.messages = [];
    $scope.list = []; //user list
    $scope.name = '';
    $scope.text = '';
    
     /* Initial connection */
    socket.on('connect', function()
    {
        $scope.setName();
        
        //socket.emit('room', room)

    });
    
    /* Creating a message */ 
    socket.on('message', function(msg)
    {
        
       console.log(msg);
       $scope.messages.push(msg);
       $scope.$apply();
      // var elem = document.getElementById('msgpane');
      // elem.scrollTop = elem.scrollHeight;
       
       
    });
    
    
    /* Getting list of active chatters */
    socket.on('list', function(names)
    {
        $scope.list = names;
        $scope.$apply();
    });
    
    /* If we aren't in the current room, go to general */
    socket.on('rooms', function(rooms)
    {
        $scope.rooms = rooms;
        
        if(!$scope.current_room)
            $scope.current_room = rooms[0];
        
        $scope.$apply();
        
    });
    
    /* Sending a message */
    $scope.send = function send()
    {
        
      console.log('Sending message: ', $scope.text);  
      socket.emit('message', {text: $scope.text, room:$scope.current_room});
      $scope.text = '';
        
    };
    
    /* Setting a chatter's name */
    $scope.setName = function setName()
    {
      console.log('Name is ', $scope.name);
      socket.emit('identify', $scope.name);
        
        
    };
    
    /* Switching a chatter's room */
    $scope.switchRoom = function(new_room)
    {
        $scope.current_room = new_room;
        socket.emit('join', $scope.current_room);
        
    };
    
    /* Searching for a specific user */
    $scope.searchmsgs = function searchmsgs()
    {
        console.log('Searching for ', $scope.finduser);
        socket.emit('search', $scope.finduser);
    };
    
    
    /* Creating a new chatroom */ 
    $scope.createRoom = function()
    {
        
        if($scope.new_name.length > 0)
        {
            superagent.post('/new_room').send({name:$scope.new_name}).end(function(err, result)
            {
                
            });
        }
        
        
        
        console.log("Create room:" + $scope.new_name);
        $scope.new_name = '';
    };
    
   
    
    /* Will probably delete this 
    socket.on('connection', function()
    {
        
        socket.on('join', function(room)
        {
            
            if(socket.room)
                socket.leave(socket.room);
            
            socket.room = room;
            socket.join(room);
        });


    });
    */
    
});