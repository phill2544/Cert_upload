

CREATE TABLE `list` (
  `List_id` int(11) NOT NULL AUTO_INCREMENT,
  `Date_use` date NOT NULL,
  `Date_return` date NOT NULL,
  `List_status` varchar(255) NOT NULL,
  `List_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Emp_id` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  `Hospital` varchar(255) NOT NULL,
  PRIMARY KEY (`List_id`),
  KEY `emphss7` (`Emp_id`),
  CONSTRAINT `emphss7` FOREIGN KEY (`Emp_id`) REFERENCES `emphss7` (`Emp_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=114 DEFAULT CHARSET=utf8mb4;


INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('73','2022-12-20','2022-12-30','return_complete','2023-01-29 22:22:22','4','3',' โรงพยาบาลพล');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('74','2022-12-22','2022-12-23','return_complete','2022-12-19 00:50:39','2','3',' โรงพยาบาลซำสูง');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('75','2022-12-19','2022-12-22','return_complete','2022-12-19 00:50:40','2','3',' โรงพยาบาลพล');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('76','2022-12-19','2022-12-21','return_complete','2022-12-19 00:57:59','2','3',' โรงพยาบาลพล');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('77','2022-12-19','2022-12-22','return_complete','2022-12-19 00:58:00','2','3',' โรงพยาบาลพล');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('78','2022-12-23','2022-12-30','return_complete','2022-12-19 00:39:53','2','3',' โรงพยาบาลพล');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('79','2022-12-22','2022-12-24','return_complete','2022-12-19 00:58:00','2','3',' โรงพยาบาลพล');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('80','2022-12-19','2022-12-21','return_complete','2022-12-19 00:58:01','2','3',' โรงพยาบาลเปือยน้อย');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('81','2022-12-20','2022-12-23','return_complete','2023-01-07 10:18:37','2','3',' โรงพยาบาลพล');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('83','2022-12-19','2022-12-22','return_complete','2022-12-19 01:13:45','2','3',' โรงพยาบาลซำสูง');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('84','2022-12-22','2023-01-06','return_complete','2022-12-23 23:35:18','2','3',' โรงพยาบาลพล');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('85','2022-12-19','2022-12-20','return_complete','2023-01-02 19:50:29','2','3',' โรงพยาบาลพล');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('86','2022-12-20','2022-12-23','return_complete','2023-01-07 10:18:38','2','3',' โรงพยาบาลซำสูง');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('87','2022-12-20','2022-12-22','return_complete','2022-12-21 01:04:52','2','3',' โรงพยาบาลเปือยน้อย');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('89','2022-12-23','2022-12-27','return_complete','2023-01-07 10:18:39','2','3',' โรงพยาบาลซำสูง');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('91','2022-12-28','2022-12-30','return_complete','2023-01-07 10:18:40','2','3',' โรงพยาบาลสมเด็จพระยุพราชกระนวน');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('92','2023-01-03','2023-01-18','return_complete','2023-01-07 10:18:41','2','3',' โรงพยาบาลซำสูง');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('93','2023-01-02','2023-01-04','return_complete','2023-01-07 11:51:37','2','3',' โรงพยาบาลซำสูง');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('110','2023-01-10','2023-01-11','return_complete','2023-01-10 00:22:31','2','3',' โรงพยาบาลเปือยน้อย  โรงพยาบาลสมเด็จพระยุพราชกระนวน');

INSERT INTO list (List_id, Date_use, Date_return, List_status, List_time, Emp_id, app_id, Hospital) VALUES ('113','2023-01-30','2023-01-30','app_return','2023-01-30 18:48:47','2','3',' โรงพยาบาลซำสูง');


CREATE TABLE `list_detail` (
  `List_id` int(11) NOT NULL,
  `Tool_id` int(11) NOT NULL,
  `note_listdetail` varchar(255) NOT NULL,
  KEY `list` (`List_id`),
  KEY `tooldata` (`Tool_id`),
  CONSTRAINT `list` FOREIGN KEY (`List_id`) REFERENCES `list` (`List_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tooldata` FOREIGN KEY (`Tool_id`) REFERENCES `tooldata` (`ToolId`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('73','1','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('73','2','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('73','3','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('73','4','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('74','5','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('74','6','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('74','7','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('74','8','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('75','1','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('75','2','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('76','3','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('76','4','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('77','9','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('77','10','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('77','11','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('77','12','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('77','13','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('78','14','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('78','15','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('79','16','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('79','17','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('80','44','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('80','45','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('80','46','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('81','1','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('81','2','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('83','3','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('83','4','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('84','6','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('85','3','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('86','4','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('87','7','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('89','7','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('91','6','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('91','9','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('91','13','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('91','16','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('91','50','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('92','10','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('93','11','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','3','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','4','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','5','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','9','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','8','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','13','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','12','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','18','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','14','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','17','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','16','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','20','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','15','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','11','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','23','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','22','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','24','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','21','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','29','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('110','10','');

INSERT INTO list_detail (List_id, Tool_id, note_listdetail) VALUES ('113','3','');
