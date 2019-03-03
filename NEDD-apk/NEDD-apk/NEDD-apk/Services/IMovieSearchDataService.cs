using NEDDApp.Models;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace NEDDApp.Services
{
    interface ITestPerDateDataService
    {

        Task<List<TestInfo>> GetTestPerDate(String query);
    }
}
