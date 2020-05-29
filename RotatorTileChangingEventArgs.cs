using System;

namespace Microsoft.Toolkit.Uwp.UI.Controls
{
    [Composable(typeof(IRotatorTileChangingEventArgs), CompositionType.Public, 65536, "Windows.Foundation.UniversalApiContract")]
    [ContractVersion(typeof(UniversalApiContract), 65536)]
    [MarshalingBehavior(MarshalingType.Agile)]
    [Threading(ThreadingModel.Both)]
    [WebHostHidden]
    public sealed class RotatorTileChangingEventArgs : IRotatorTileChangingEventArgs
    {
        public RotatorTileChangingEventArgs(object oldItem, object newItem)
        {
            OldItem = oldItem;
            NewItem = newItem;
        }
        public object OldItem { get; private set; }
        public object NewItem { get; private set; }
    }

}
