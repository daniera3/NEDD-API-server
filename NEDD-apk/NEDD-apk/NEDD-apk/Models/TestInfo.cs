using System;
using System.Collections.Generic;
using System.Text;

namespace NEDDApp.Models
{
    public class TestInfo
    {
        public String user { get; set; }
        public String Line { get; set; }
        public String Sey { get; set; }
        public bool Getpass()
        {
            return (this.Line == this.Sey && Line.Length!=0 && Sey.Length != 0);
        }
    }
}
