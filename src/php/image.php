<?php
require_once 'dbConfig.php'; 
 
// Get image data from database
$result = $db->query("SELECT image_url FROM Museums WHERE id = 1"); 
?>

<?php if($result->num_rows > 0){ ?> 
    <div class="column"> 
        <?php while($row = $result->fetch_assoc()){ ?> 
            <img src="data:image/jpg;charset=utf8;base64,<?php echo base64_encode($row['image']); ?>" /> 
        <?php } ?> 
    </div> 
<?php }else{ ?> 
    <p class="status error">Image(s) not found...</p> 
<?php } ?>