package Game;

public class BurnStackPoker{
    public static void main(String[] args){
        Player[] players = {new Player("User"), new Player("Computer")};
        Table gameTable = new Table(players);
        gameTable.startGame();
    }
}