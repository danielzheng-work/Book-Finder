package frame;

import java.awt.EventQueue;
import java.awt.FontMetrics;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.util.List;
import java.util.Map;

import javax.imageio.ImageIO;
import javax.swing.BorderFactory;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;

import service.OpeationService;
import service.impl.OprationServiceImpl;

public class index extends JFrame {

	private JPanel contentPane;
	private JTextField textField;
	private JLabel lblNewLabel_1;
	private JComboBox comboBox;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					index frame = new index();
					frame.setVisible(true);
					frame.setTitle("Book Finder");
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public index() {
		
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 450, 413);
		setLocationRelativeTo(null);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		String[] strings = {"ASIN Cloud","Keyword Freq","ASIN Convert", "ASIN Relations"};
		comboBox = new JComboBox(strings);
		comboBox.setBounds(17, 27, 94, 27);
		contentPane.add(comboBox);
		
		textField = new JTextField();
		textField.setBounds(123, 22, 181, 35);
		contentPane.add(textField);
		textField.setColumns(10);
		
		JButton btnNewButton = new JButton("Search");
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				String bookName = textField.getText();
				OpeationService operation = new OprationServiceImpl();
				if("ASIN Cloud".equals(comboBox.getSelectedItem().toString())) {
					try {
						if(operation.getKeyAndWordCloudByBookName(bookName)) {
							File file = new File("");
					        String filePath = file.getCanonicalPath();
					        Icon icon = new ImageIcon(ImageIO.read(new File(filePath+"/py/word_cloud.png")));
							lblNewLabel_1.setIcon(icon);
							lblNewLabel_1.repaint();
						}

					} catch (Exception e1) {
						e1.printStackTrace();
					}
				}else if("Keyword Freq".equals(comboBox.getSelectedItem().toString())){
					Map<String,Object> map= operation.init(bookName);
					if((boolean) map.get("flag")) {
						List<String> lines = (List<String>) map.get("data");
						StringBuilder builder = new StringBuilder("<html>");
						for(String line:lines) {
							builder.append(line.trim()).append("<br/>");
						}
						builder.append("</html>");
						lblNewLabel_1.setIcon(null);
						lblNewLabel_1.setText(builder.toString());
						lblNewLabel_1.repaint();
					}
				}else if("ASIN Convert".equals(comboBox.getSelectedItem().toString())){
					Map<String,Object> map = operation.getWebScraperByBookName(bookName);
					if((boolean) map.get("flag")) {
						try {
							List<String> lines = (List<String>) map.get("data");
							String ss = String.join(",", lines);
							if(lines!=null && lines.size()!=0) {
								lblNewLabel_1.setIcon(null);
								JlabelSetText(lblNewLabel_1,ss.replace("\n", "").trim());
								lblNewLabel_1.repaint();
							}
						} catch (InterruptedException e1) {
							e1.printStackTrace();
						}
						
					}
				}
				else {
					Map<String,Object> map = operation.getMatchingBooks(bookName);
					if((boolean) map.get("flag")) {
						List<String> lines = (List<String>) map.get("data");
						StringBuilder builder = new StringBuilder("<html>");
						for(String line:lines) {
							builder.append(line.trim()).append("<br/>");
						}
						builder.append("</html>");
						lblNewLabel_1.setIcon(null);
						lblNewLabel_1.setText(builder.toString());
						lblNewLabel_1.repaint();
					}
				}				
				
				
				
			}
		});
		btnNewButton.setBounds(316, 24, 117, 33);
		contentPane.add(btnNewButton);
//		ImageIcon img=new ImageIcon(("../../../image/cloud.png"));
//		img.setImage(img.getImage().getScaledInstance(414, 200,Image.SCALE_DEFAULT));
		lblNewLabel_1 = new JLabel();
		lblNewLabel_1.setBounds(17, 87, 414, 280);
		contentPane.add(lblNewLabel_1);
		
	}
	void JlabelSetText(JLabel jLabel, String longString) 
			   throws InterruptedException {
				StringBuilder builder = new StringBuilder("<html>");
				char[] chars = longString.toCharArray();
				FontMetrics fontMetrics = jLabel.getFontMetrics(jLabel.getFont());
				int start = 0;
				int len = 0;
				while (start + len < longString.length()) {
					while (true) {
						len++;
						if (start + len > longString.length())break;
						if (fontMetrics.charsWidth(chars, start, len) 
						      > jLabel.getWidth()) {
							break;
						}
					}
					builder.append(chars, start, len-1).append("<br/>");
					start = start + len - 1;
					len = 0;
				}
				builder.append(chars, start, longString.length()-start);
				builder.append("</html>");
				jLabel.setText(builder.toString());
			}
}
