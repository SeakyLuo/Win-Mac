using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InvincibleGuard : Trigger {

	public override void BloodThirsty ()
	{
		GameInfo.actions [InfoLoader.playerID]++;
	}
}
