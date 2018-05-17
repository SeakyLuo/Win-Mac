using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LandmineEngineer : Trigger {

	public override void AtEnemyBottom ()
	{
		GameController.PlaceTrap (piece.location, Database.RandomTrap (), InfoLoader.playerID);
	}
}
