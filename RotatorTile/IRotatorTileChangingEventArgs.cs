using System;

namespace Microsoft.Toolkit.Uwp.UI.Controls
{
    [ContractVersion(typeof(UniversalApiContract), 65536)]
    [ExclusiveTo(typeof(RotatorTileChangingEventArgs))]
    [GuidAttribute(1553488582, 55298, 19256, 162, 35, 191, 7, 12, 67, 254, 223)]
    [WebHostHidden]
    internal interface IRotatorTileChangingEventArgs
    {
        object OldItem { get; }
        object NewItem { get; }
    }
}
